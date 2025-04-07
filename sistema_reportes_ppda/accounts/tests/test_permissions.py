from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from management.models import Body


class UserPermissionsTestCase(APITestCase):
    def setUp(self):
        self.superuser = self._create_superuser()

        self.body = Body.objects.create(
            name="SEREMI TEST",
            created_by=self.superuser
        )

        self.user_regular = CustomUser.objects.create_user(
            username="usuario",
            password="test123",
            email="usuario@test.cl",
            rut="12345678-5",
            body=self.body
        )

        self.user_sma = CustomUser.objects.create_user(
            username="smauser",
            password="test123",
            email="sma@test.cl",
            rut="11111111-1",
            body=self.body,
            is_staff=True
        )

        self.url_list = reverse("user-list")
        self.url_detail = lambda user_id: reverse("user-detail", args=[user_id])

    def _create_superuser(self):
        return CustomUser.objects.create_superuser(
            username="admin", password="admin123", email="admin@sma.cl", rut="99999999-9"
        )

    def authenticate(self, username, password):
        """Helper para autenticación vía JWT"""
        response = self.client.post(reverse("token_obtain_pair"), {
            "username": username,
            "password": password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_regular_user_cannot_list_users(self):
        self.authenticate("usuario", "test123")
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sma_user_can_list_users(self):
        self.authenticate("smauser", "test123")
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve_own_profile(self):
        self.authenticate("usuario", "test123")
        response = self.client.get(self.url_detail(self.user_regular.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_retrieve_other_profile(self):
        self.authenticate("usuario", "test123")
        response = self.client.get(self.url_detail(self.user_sma.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sma_can_delete_user(self):
        self.authenticate("smauser", "test123")
        response = self.client.delete(self.url_detail(self.user_regular.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_regular_user_cannot_delete_other_user(self):
        self.authenticate("usuario", "test123")
        response = self.client.delete(self.url_detail(self.user_sma.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
