from django.contrib.auth.models import AbstractUser
from django.db import models
from management.models import Body

class CustomUser(AbstractUser):
    """
    Represents a system user representing a natural person (RUT) that belongs to 
    a sectorial body.
    """
    
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True)
    body = models.ForeignKey(Body, on_delete=models.CASCADE, related_name='body_users', null=True, blank=True)

    def clean(self):
        """ Validar formato y número verificador. """
        # if not validate_rut(self.rut):
        #     raise ValidationError("Formato o número verificador inválido.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
