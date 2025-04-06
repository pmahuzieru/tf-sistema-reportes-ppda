from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from management.models import Body


class UserProfileEditTestCase(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            username="admin",
            password="admin123",
            email="admin@sma.cl",
            rut="11111111-1"
        )

        self.body = Body.objects.create(name="SEREMI TEST", created_by=self.admin)

        self.user = CustomUser.objects.create_user(
            username="usuario",
            password="test123",
            email="usuario@test.cl",
            rut="12345678-5",
            body=self.body
        )

        self.other_user = CustomUser.objects.create_user(
            username="otro",
            password="test123",
            email="otro@test.cl",
            rut="22222222-2",
            body=self.body
        )

        self.url_detail = lambda user_id: reverse("user-detail", args=[user_id])

    def authenticate(self, username, password):
        response = self.client.post(reverse("token_obtain_pair"), {
            "username": username,
            "password": password
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_user_can_edit_own_profile(self):
        self.authenticate("usuario", "test123")
        response = self.client.patch(self.url_detail(self.user.id), {
            "first_name": "NuevoNombre"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "NuevoNombre")

    def test_user_cannot_edit_other_profile(self):
        self.authenticate("usuario", "test123")
        response = self.client.patch(self.url_detail(self.other_user.id), {
            "first_name": "Hackeado"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_edit_any_profile(self):
        self.authenticate("admin", "admin123")
        response = self.client.patch(self.url_detail(self.user.id), {
            "first_name": "EditadoPorAdmin"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "EditadoPorAdmin")
