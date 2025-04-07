from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from management.models import Body
from accounts.models import CustomUser


class RegisterUserAPITestCase(APITestCase):
    def setUp(self):
        # Crea un organismo (Body) para asignar al usuario
        self.body = Body.objects.create(
            name="SEREMI TEST",
            created_by=self._create_admin()
        )
        self.url = reverse("register_users-list")

    def _create_admin(self):
        return CustomUser.objects.create_superuser(
            username="admin",
            password="admin123",
            email="admin@sma.cl",
            rut="11111111-1"
        )

    def test_register_valid_user(self):
        """Debe permitir registrar un usuario nuevo con RUT válido."""
        data = {
            "username": "usuario1",
            "password": "ClaveSegura123",
            "email": "usuario1@test.cl",
            "rut": "12345678-5",
            "first_name": "Juan",
            "last_name": "Pérez",
            "body": self.body.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username="usuario1").exists())

    def test_register_user_with_duplicate_rut_fails(self):
        """Debe fallar si el RUT ya existe."""
        CustomUser.objects.create_user(
            username="duplicado",
            password="123456",
            rut="12345678-5",
            email="ya@existe.cl",
            body=self.body
        )
        data = {
            "username": "nuevo_usuario",
            "password": "ClaveSegura123",
            "email": "nuevo@test.cl",
            "rut": "12345678-5",  # Mismo RUT que el anterior
            "first_name": "Pedro",
            "last_name": "González",
            "body": self.body.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("RUT already exists.", response.data.get("message", ""))

    def test_register_user_with_duplicate_username_fails(self):
        """Debe fallar si el username ya existe."""
        CustomUser.objects.create_user(
            username="usuario1",
            password="123456",
            rut="12345678-5",
            email="ya@existe.cl",
            body=self.body
        )
        data = {
            "username": "usuario1",  # mismo username
            "password": "ClaveSegura123",
            "email": "otro@test.cl",
            "rut": "87654321-9",
            "first_name": "Luis",
            "last_name": "Pérez",
            "body": self.body.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Username already exists.", response.data.get("message", ""))
