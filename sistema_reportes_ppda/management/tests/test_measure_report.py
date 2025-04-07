from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from management.models import (
    EnvironmentalPlan, Measure, MeasureReport, Body, BodyMeasure
)


class MeasureReportViewSetTests(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            username="admin", password="admin123", email="admin@sma.cl", rut="11111111-1"
        )

        self.body = Body.objects.create(name="SEREMI RM", created_by=self.admin)

        self.user = CustomUser.objects.create_user(
            username="organismo", password="test123", email="user@seremi.cl", rut="12345678-5", body=self.body
        )

        self.plan = EnvironmentalPlan.objects.create(
            name="Plan de Prueba", short_name="PLAN", type="PPDA", created_by=self.admin
        )

        self.measure = Measure.objects.create(
            reference_PDA=self.plan,
            measure_type="R",
            short_name="Reducción",
            indicator="Tasa",
            calculation_formula="X/Y",
            value_type="integer",
            reporting_frequency="Anual",
            verification_methods="Certificado",
            created_by=self.admin
        )

        # Asignar el organismo a esta medida
        BodyMeasure.objects.create(
            fk_measure=self.measure,
            fk_body=self.body,
            is_reporter=True,
            active=True,
            created_by=self.admin
        )

        self.url_list = reverse("report-list")

    def authenticate(self, username, password):
        response = self.client.post(reverse("token_obtain_pair"), {
            "username": username,
            "password": password
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_authenticated_user_can_list_reports(self):
        self.authenticate("organismo", "test123")
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_report_if_assigned(self):
        self.authenticate("organismo", "test123")
        response = self.client.post(self.url_list, {
            "measure": self.measure.id,
            "reported_value": "123"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        report = MeasureReport.objects.first()
        self.assertEqual(report.measure, self.measure)
        self.assertEqual(report.created_by, self.user)

    def test_user_cannot_report_if_not_assigned(self):
        other_body = Body.objects.create(name="Otro", created_by=self.admin)
        other_user = CustomUser.objects.create_user(
            username="otro", password="otro123", email="otro@seremi.cl", rut="87654321-0", body=other_body
        )
        self.authenticate("otro", "otro123")
        response = self.client.post(self.url_list, {
            "measure": self.measure.id,
            "reported_value": "99"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
