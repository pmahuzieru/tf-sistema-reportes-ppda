from rest_framework.permissions import BasePermission

SUPERINTENDENCIA_DEL_MEDIO_AMBIENTE = "Superintendencia del Medio Ambiente"


class IsSMAUser(BasePermission):
    """
    Allows permission only to users that represent the SMA.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "body", None).name.strip()
            == SUPERINTENDENCIA_DEL_MEDIO_AMBIENTE
        )
