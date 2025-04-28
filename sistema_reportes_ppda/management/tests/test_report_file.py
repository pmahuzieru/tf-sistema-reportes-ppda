from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import CustomUser
from management.models import (
    EnvironmentalPlan, Measure, Body, BodyMeasure, MeasureReport, ReportFile
)


class ReportFileViewSetTests(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            username="admin", password="admin123", email="admin@sma.cl", rut="11111111-1"
        )

        self.body = Body.objects.create(name="SEREMI RM", created_by=self.admin)

        self.user = CustomUser.objects.create_user(
            username="organismo", password="test123", email="org@seremi.cl", rut="12345678-5", body=self.body
        )

        self.plan = EnvironmentalPlan.objects.create(
            name="Plan", short_name="PLAN", type="PPDA", created_by=self.admin
        )

        self.measure = Measure.objects.create(
            reference_PDA=self.plan,
            measure_type="R",
            short_name="M1",
            indicator="Indicador",
            calculation_formula="A+B",
            value_type="integer",
            reporting_frequency="Anual",
            verification_methods="Certificado",
            created_by=self.admin
        )

        BodyMeasure.objects.create(
            fk_body=self.body,
            fk_measure=self.measure,
            is_reporter=True,
            active=True,
            created_by=self.admin
        )

        self.report = MeasureReport.objects.create(
            measure=self.measure,
            reported_value="100",
            created_by=self.user
        )

        self.url_list = reverse("file-list")

    def authenticate(self, username, password):
        response = self.client.post(reverse("token_obtain_pair"), {
            "username": username,
            "password": password
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_user_can_upload_file_to_own_report(self):
        self.authenticate("organismo", "test123")

        file_data = SimpleUploadedFile("respaldo.pdf", b"contenido", content_type="application/pdf")

        response = self.client.post(self.url_list, {
            "report": self.report.id,
            "description": "Archivo de respaldo",
            "file": file_data
        }, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReportFile.objects.count(), 1)
        self.assertEqual(ReportFile.objects.first().created_by, self.user)

    def test_user_cannot_upload_file_to_others_report(self):
        other_body = Body.objects.create(name="Otro", created_by=self.admin)
        other_user = CustomUser.objects.create_user(
            username="otro", password="otro123", email="otro@seremi.cl", rut="98765432-1", body=other_body
        )
        self.authenticate(other_user.username, "otro123")

        file_data = SimpleUploadedFile("respaldo2.pdf", b"otro archivo", content_type="application/pdf")

        response = self.client.post(self.url_list, {
            "report": self.report.id,
            "description": "No debería funcionar",
            "file": file_data
        }, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
