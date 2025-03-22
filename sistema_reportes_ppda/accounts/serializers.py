from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import CustomUser
from accounts.utils import validate_rut
from management.models import Body

class CustomUserSerializer(serializers.ModelSerializer):
    # Evitar que se exponga el password
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    
    email = serializers.EmailField(required=True)
    rut = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    body = serializers.PrimaryKeyRelatedField(queryset=Body.objects.all())

    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "email", "rut", "first_name", "last_name", "is_active", "body"]

    def create(self, validated_data):
        """Crea un usuario con la contraseña hasheada automáticamente."""
        password = validated_data.pop("password")
        return CustomUser.objects.create_user(password=password, **validated_data)

    def validate_rut(self, value):
        """Valida el RUT antes de guardar."""
        if not validate_rut(value):
            raise serializers.ValidationError("RUT inválido.")
        return value
