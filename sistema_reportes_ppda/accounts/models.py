from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from accounts.utils import validate_rut

class CustomUser(AbstractUser):
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True)

    def clean(self):
        """ Validar formato y número verificador. """
        # if not validate_rut(self.rut):
        #     raise ValidationError("Formato o número verificador inválido.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
