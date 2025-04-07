from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from management.models import EnvironmentalPlan
from reporting.models import ProgressReport, ProgressReportData
from datetime import date


class ProgressReportTests(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            username="admin", password="admin123", email="admin@sma.cl", rut="11111111-1"
        )

        self.user = CustomUser.objects.create_user(
            username="usuario", password="test123", email="user@test.cl", rut="22222222-2"
        )

        self.plan = EnvironmentalPlan.objects.create(
            name="Plan de Prueba", short_name="PP", type="PDA", created_by=self.admin
        )

        self.url_list = reverse("progressreport-list")

    def authenticate(self, username, password):
        response = self.client.post(reverse("token_obtain_pair"), {
            "username": username,
            "password": password
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_non_sma_user_cannot_create_progress_report(self):
        self.authenticate("usuario", "test123")
        response = self.client.post(self.url_list, {
            "name": "Reporte Q1",
            "environmental_plan_id": self.plan.id,
            "publication_date": date.today()
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sma_can_create_progress_report_and_triggers_data_generation(self):
        self.authenticate("admin", "admin123")
        response = self.client.post(self.url_list, {
            "name": "Reporte Q1",
            "environmental_plan_id": self.plan.id,
            "publication_date": date.today()
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        report = ProgressReport.objects.get(name="Reporte Q1")
        self.assertEqual(report.created_by, self.admin)
        self.assertTrue(report.data_created)
        self.assertTrue(hasattr(report, "data"))
        self.assertIsInstance(report.data, ProgressReportData)

def test_progress_report_data_reflects_measure_reports(self):
    # Setup: autenticar como admin
    self.authenticate("admin", "admin123")

    # Crear medida
    from management.models import Measure, Body, BodyMeasure, MeasureReport
    from reporting.models import ProgressReportData

    body = Body.objects.create(name="SEREMI TEST", created_by=self.admin)
    user = CustomUser.objects.create_user(
        username="seremi_user", password="seremi123", rut="12345678-5", body=body
    )

    measure = Measure.objects.create(
        reference_PDA=self.plan,
        measure_type="R",
        short_name="Reducción PM2.5",
        indicator="Toneladas",
        calculation_formula="X/Y",
        value_type="integer",
        reporting_frequency="Anual",
        verification_methods="Certificado",
        created_by=self.admin
    )

    BodyMeasure.objects.create(
        fk_body=body,
        fk_measure=measure,
        is_reporter=True,
        active=True,
        created_by=self.admin
    )

    # Autenticar como organismo y reportar
    self.authenticate("seremi_user", "seremi123")
    self.client.post(reverse("report-list"), {
        "measure": measure.id,
        "reported_value": "42"
    })

    # Volver a autenticarse como admin para crear el progress report
    self.authenticate("admin", "admin123")
    response = self.client.post(reverse("progressreport-list"), {
        "name": "Avance Abril",
        "environmental_plan_id": self.plan.id,
        "publication_date": "2025-04-01"
    })

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    report_id = response.data["id"]

    # Obtener datos generados
    progress_data = ProgressReportData.objects.get(progress_report__id=report_id)
    self.assertIn("measures", progress_data.data)
    self.assertGreater(len(progress_data.data["measures"]), 0)

    # Validamos que incluya nuestra medida y el valor reportado
    reported_measures = progress_data.data["measures"]
    medida_encontrada = any(str(measure.id) in str(m) and "42" in str(m) for m in reported_measures)
    self.assertTrue(medida_encontrada, "El valor reportado no aparece en el resumen")

