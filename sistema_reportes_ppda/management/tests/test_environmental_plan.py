from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from management.models import EnvironmentalPlan


class EnvironmentalPlanTests(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            username="admin",
            password="admin123",
            email="admin@sma.cl",
            rut="11111111-1"
        )

        self.user = CustomUser.objects.create_user(
            username="usuario",
            password="test123",
            email="usuario@test.cl",
            rut="22222222-2"
        )

        self.url_list = reverse("environmentalplan-list")

    def authenticate(self, username, password):
        """Helper para autenticación JWT"""
        response = self.client.post(reverse("token_obtain_pair"), {
            "username": username,
            "password": password
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_authenticated_user_can_list_plans(self):
        self.authenticate("usuario", "test123")
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_sma_user_cannot_create_plan(self):
        self.authenticate("usuario", "test123")
        response = self.client.post(self.url_list, {
            "name": "Plan No Autorizado",
            "short_name": "PNA",
            "type": "PPDA"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sma_can_create_plan(self):
        self.authenticate("admin", "admin123")
        response = self.client.post(self.url_list, {
            "name": "Plan de Prueba",
            "short_name": "PLAN1",
            "type": "PDA"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EnvironmentalPlan.objects.count(), 1)
        plan = EnvironmentalPlan.objects.first()
        self.assertEqual(plan.created_by, self.admin)

    def test_sma_can_update_plan(self):
        self.authenticate("admin", "admin123")
        plan = EnvironmentalPlan.objects.create(
            name="Plan Original",
            short_name="ORIG",
            type="PPA",
            created_by=self.admin
        )
        url = reverse("environmentalplan-detail", args=[plan.id])
        response = self.client.patch(url, {"name": "Plan Actualizado"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plan.refresh_from_db()
        self.assertEqual(plan.name, "Plan Actualizado")
        self.assertEqual(plan.updated_by, self.admin)
