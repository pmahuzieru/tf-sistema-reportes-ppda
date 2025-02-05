from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import CustomUser
from accounts.utils import validate_rut

class CustomUserSerializer(serializers.ModelSerializer):
    # Evitar que se exponga el password
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "email", "rut", "first_name", "last_name", "is_active"]

    def create(self, validated_data):
        """Crea un usuario con la contraseña hasheada automáticamente."""
        password = validated_data.pop("password")
        return CustomUser.objects.create_user(password=password, **validated_data)

    def validate_rut(self, value):
        """Valida el RUT antes de guardar."""
        if not validate_rut(value):
            raise serializers.ValidationError("RUT inválido.")
        return value
