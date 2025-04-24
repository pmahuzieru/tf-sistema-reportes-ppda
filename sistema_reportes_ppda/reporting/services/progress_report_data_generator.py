from collections import defaultdict

from django.utils.timezone import localtime

from management.models import Body
from reporting.models import ProgressReportData


class ProgressReportDataGenerator:
    """
    Stores the main business logic to build the required metrics and data for the
    'Informe de Estado de Avance'.
    """
    
    def __init__(self, progress_report):
        self.progress_report = progress_report
        self.environmental_plan = progress_report.environmental_plan

    def get_measure_status_data(self):
        """
        Retrieves the Plan's measures and their latest reported value.
        """
        measures = self.environmental_plan.measures.all()
        measure_status_data = {}

        for measure in measures:
            latest_report = measure.get_latest_report()

            measure_status_data[str(measure.id)] = {
                "measure_short_name": measure.short_name,
                "reported_value": (
                    latest_report.reported_value if latest_report else None
                ),
                "reported_at": (
                    localtime(latest_report.created_at).isoformat()
                    if latest_report
                    else None
                ),
            }

        return measure_status_data

    def get_measure_type_count_data(self):
        """
        Counts how many measures are for each measure type.
        """
        measures = self.environmental_plan.measures.all()

        measure_type_count = {}

        for measure in measures:
            measure_type = measure.measure_type
            measure_type_count[measure_type] = (
                measure_type_count.get(measure_type, 0) + 1
            )

        return measure_type_count

    def get_body_participation_data(self):
        """
        Obtains information on the participation of each Sectorial Body in the
        different measure types.
        """
        measures = self.environmental_plan.measures.all()

        # Create a defaultdict for {body: {measure_type: count}} to avoid KeyError
        body_measure_type_count = defaultdict(lambda: defaultdict(int))

        for measure in measures:
            measure_type = measure.measure_type

            # Get all Bodies related to the measure
            bodies = Body.objects.filter(body_bodymeasure__fk_measure=measure)

            for body in bodies:
                body_measure_type_count[str(body.id)][measure_type] += 1

        return body_measure_type_count

    def get_measure_completion_status_by_type(self):
        """
        Builds a dict with the amount of measures with at least one report and of those
        not reported upon, for each measure type.
        """
        measures = self.environmental_plan.measures.all()

        # {measure_type: {reported: n, not_reported: m}}
        measure_completion_status = defaultdict(lambda: defaultdict(int))

        for measure in measures:
            measure_type = measure.measure_type

            if measure.has_reports():
                measure_completion_status[measure_type]["reported"] += 1
            else:
                measure_completion_status[measure_type]["not_reported"] += 1

        return measure_completion_status

    def generate(self):
        """
        Generates the required data for the ProgressReport and stores it in the database.
        """

        progress_report_data = {
            "measure_status_data": self.get_measure_status_data(),
            "measure_type_count_data": self.get_measure_type_count_data(),
            "body_participation_data": self.get_body_participation_data(),
            "measure_completion_status_by_type": self.get_measure_completion_status_by_type(),
        }

        ProgressReportData.objects.create(
            progress_report=self.progress_report, data=progress_report_data
        )
