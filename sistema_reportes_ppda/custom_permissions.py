from rest_framework.permissions import BasePermission

from management.models import BodyMeasure, Measure, MeasureReport


SUPERINTENDENCIA_DEL_MEDIO_AMBIENTE = "Superintendencia del Medio Ambiente"


def is_sma(user):
    """
    Checks whether the User's body corresponds to the SMA.
    """
    user_body = getattr(user, "body", None)

    if not user_body:
        return False

    return user_body.name.strip() == SUPERINTENDENCIA_DEL_MEDIO_AMBIENTE


class IsSMAUser(BasePermission):
    """
    Allows permission only to users that represent the SMA.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and is_sma(request.user)


class IsSMAOrSelf(BasePermission):
    """
    Allows complete User listing access for SMA users, but others only to their own information.
    """
    
    def has_object_permission(self, request, view, obj):
        if is_sma(request.user):
            True
        return obj == request.user
        
    

class IsAssignedToReportMeasure(BasePermission):
    """
    Allows permission only if the user's Body is assigned to report the Measure.
    """

    def has_permission(self, request, view):
        """
        For SMA users, full access.
        For Body users, only if measure is assigned for theirs to report.
        """
        if is_sma(request.user):
            return True
        
        measure_id = request.data.get('measure')
        measure = Measure.objects.get(id=measure_id)
        user_body = request.user.body
        
        is_assigned = BodyMeasure.objects.filter(
            fk_measure=measure,
            fk_body=user_body,
            is_reporter=True
        ).exists()
        
        return is_assigned
        
        
class ReportIsTheirs(BasePermission):
    """
    Allows permission if the related measure Report is from the User's body.
    For SMA users, full access.
    """
    def has_permission(self, request, view):
        
        if is_sma(request.user):
            return True
        
        report_id = request.data.get("report")
        report = MeasureReport.objects.get(id=report_id)
        related_measure = report.measure
        user_body = request.user.body
        
        is_assigned = BodyMeasure.objects.filter(
            fk_measure=related_measure,
            fk_body=user_body,
            is_reporter=True
        ).exists()
        
        return is_assigned