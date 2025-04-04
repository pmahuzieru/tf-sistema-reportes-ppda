from django.utils.timezone import localtime
from management.models import Measure, MeasureReport
from reporting.models import ProgressReportData


class ProgressReportDataGenerator:
    def __init__(self, progress_report):
        self.progress_report = progress_report
        self.environmental_plan = progress_report.environmental_plan

    def get_measure_status_data(self):
        """
        Retrieves the Plan's measures and their latest reported value.
        """
        measures = Measure.objects.filter(reference_PDA=self.environmental_plan)
        measure_status_data = {}

        for measure in measures:
            latest_report = (
                MeasureReport.objects.filter(measure=measure)
                .order_by("-created_at")
                .first()
            )

            measure_status_data[str(measure.id)] = {
                "measure_short_name": measure.short_name,
                "reported_value": (
                    latest_report.reported_value if latest_report else None
                ),
                "reported_at": (
                    localtime(latest_report.created_at) if latest_report else None
                ),
            }

        return measure_status_data

    def get_measure_type_count_data(self):
        """
        Counts how many measures are for each measure type.
        """
        measures = Measure.objects.filter(reference_PDA=self.environmental_plan)

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
        pass
    
    def get_measure_completion_status_by_type(self):
        """
        Builds a dict with the amount of measures with at least one report and of those
        not reported upon, for each measure type.
        """
        pass

    def generate(self):

        progress_report_data = {
            "measure_status_data": self.get_measure_status_data(),
            "measure_type_count_data": self.get_measure_type_count_data(),
            "body_participation_data": self.get_body_participation_data(),
        }

        ProgressReportData.objects.create(
            progress_report=self.progress_report, data=progress_report_data
        )
