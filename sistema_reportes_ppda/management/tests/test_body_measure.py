from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from management.models import EnvironmentalPlan, Measure, Body, BodyMeasure


class BodyMeasureViewSetTests(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            username="admin", password="admin123", email="admin@sma.cl", rut="11111111-1"
        )

        self.user = CustomUser.objects.create_user(
            username="usuario", password="test123", email="usuario@test.cl", rut="22222222-2"
        )

        self.body = Body.objects.create(name="SEREMI RM", created_by=self.admin)

        self.plan = EnvironmentalPlan.objects.create(
            name="Plan de Prueba", short_name="PP", type="PPDA", created_by=self.admin
        )

        self.measure = Measure.objects.create(
            reference_PDA=self.plan,
            measure_type="R",
            short_name="Medida 1",
            indicator="Indicador 1",
            calculation_formula="A/B",
            value_type="integer",
            reporting_frequency="Anual",
            verification_methods="Certificado",
            created_by=self.admin
        )

        self.url_list = reverse("bodymeasure-list")

    def authenticate(self, username, password):
        response = self.client.post(reverse("token_obtain_pair"), {
            "username": username,
            "password": password
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_authenticated_user_can_list_bodymeasures(self):
        self.authenticate("usuario", "test123")
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_sma_cannot_create_bodymeasure(self):
        self.authenticate("usuario", "test123")
        response = self.client.post(self.url_list, {
            "fk_body": self.body.id,
            "fk_measure": self.measure.id,
            "is_reporter": True,
            "active": True
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sma_can_create_bodymeasure(self):
        self.authenticate("admin", "admin123")
        response = self.client.post(self.url_list, {
            "fk_body": self.body.id,
            "fk_measure": self.measure.id,
            "is_reporter": True,
            "active": True
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assignment = BodyMeasure.objects.first()
        self.assertEqual(assignment.fk_body, self.body)
        self.assertEqual(assignment.fk_measure, self.measure)
        self.assertEqual(assignment.created_by, self.admin)
