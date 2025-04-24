from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from management.models import EnvironmentalPlan, Measure


class MeasureViewSetTests(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            username="admin", password="admin123", email="admin@sma.cl", rut="11111111-1"
        )

        self.user = CustomUser.objects.create_user(
            username="usuario", password="test123", email="usuario@test.cl", rut="22222222-2"
        )

        self.plan = EnvironmentalPlan.objects.create(
            name="Plan Test",
            short_name="PT",
            type="PPDA",
            created_by=self.admin
        )

        self.url_list = reverse("measure-list")

    def authenticate(self, username, password):
        response = self.client.post(reverse("token_obtain_pair"), {
            "username": username,
            "password": password
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def get_valid_payload(self):
        return {
            "reference_PDA": self.plan.id,
            "measure_type": "R",
            "short_name": "Reducción emisiones",
            "indicator": "Tasa de emisión anual",
            "calculation_formula": "X/Y * 100",
            "value_type": "decimal",
            "reporting_frequency": "Anual",
            "verification_methods": "Certificado de emisiones",
            "is_regulatory": True
        }

    def test_authenticated_user_can_list_measures(self):
        self.authenticate("usuario", "test123")
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_sma_user_cannot_create_measure(self):
        self.authenticate("usuario", "test123")
        response = self.client.post(self.url_list, self.get_valid_payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sma_user_can_create_measure(self):
        self.authenticate("admin", "admin123")
        response = self.client.post(self.url_list, self.get_valid_payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        measure = Measure.objects.first()
        self.assertEqual(measure.created_by, self.admin)
        self.assertEqual(measure.reference_PDA, self.plan)

    def test_sma_can_update_measure(self):
        self.authenticate("admin", "admin123")
        measure = Measure.objects.create(
            reference_PDA=self.plan,
            measure_type="E",
            short_name="Estudio piloto",
            indicator="Estudios realizados",
            calculation_formula="SUM(X)",
            value_type="integer",
            reporting_frequency="Anual",
            verification_methods="Informe técnico",
            is_regulatory=False,
            created_by=self.admin
        )
        url = reverse("measure-detail", args=[measure.id])
        response = self.client.patch(url, {"short_name": "Estudio actualizado"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        measure.refresh_from_db()
        self.assertEqual(measure.short_name, "Estudio actualizado")
        self.assertEqual(measure.updated_by, self.admin)
