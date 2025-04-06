from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from custom_permissions import IsAdminOrSMAOrSelf, IsSMAUserOrAdmin
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Usuarios (administración)"],
    summary="Administración de usuarios del sistema",
    description="""
Este endpoint permite consultar, modificar o eliminar usuarios registrados en el sistema.

Está diseñado principalmente para uso de usuarios **SMA o administradores**, aunque cada usuario puede ver o modificar su propio perfil.

### Permisos:
- `list`: solo usuarios de la SMA pueden ver la lista completa de usuarios.
- `retrieve`: cualquier usuario puede ver su propio perfil.
- `update`/`partial_update`: cualquier usuario puede modificar su propio perfil.
- `destroy`: solo SMA puede eliminar usuarios.

### Campos relevantes:
- `username`, `email`, `first_name`, `last_name`, `rut`
- `body`: organismo al que pertenece el usuario
"""
)
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """
        - Solo los usuarios de la SMA pueden listar (`list`) todos los usuarios.
        - Los usuarios solo pueden ver (`retrieve`) y modificar (`update`, `partial_update`) su propio perfil.
        - Solo los SMA pueden eliminar (`destroy`) usuarios.
        """
        if self.action == "list":
            return [IsSMAUserOrAdmin()]  # Solo SMA puede ver la lista
        if self.action in ["update", "partial_update", "retrieve", "destroy"]:
            return [IsAdminOrSMAOrSelf()]  # SMA puede hacer todo, otros solo su perfil

        return super().get_permissions()
    

@extend_schema(
    tags=["Usuarios (registro)"],
    summary="Registro de nuevos usuarios",
    description="""
Este endpoint permite que los usuarios se registren en el sistema proporcionando los datos necesarios.
Está abierto al público y permite la creación de un nuevo usuario, con validaciones personalizadas para asegurarse
de que el nombre de usuario y el RUT no se repitan.

### Permisos:
- `POST`: Acceso abierto a todos los usuarios, sin autenticación previa.
- El registro solo será exitoso si no existe un usuario con el mismo nombre de usuario o RUT.

### Validaciones:
- Se valida que el `username` no esté ya registrado.
- Se valida que el `rut` no esté ya registrado.
- El `rut` debe ser válido según el algoritmo Módulo 11 chileno.
- Se acepta en formatos como `12345678-5`, `12.345.678-5` o `123456785`.
- El sistema lo transformará internamente al formato estándar: `12345678-5`.

### Campos requeridos:
- `username`: Nombre de usuario único.
- `email`: Dirección de correo electrónico válida.
- `rut`: RUT único, con validación específica.
- `first_name`: Nombre del usuario.
- `last_name`: Apellido del usuario.
"""
)
class RegisterUserModelViewSet(viewsets.ModelViewSet):
    # It makes sence that the registration should be public, so i left de auth comment in case our hypothesis 
    # is wrong

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def get_permissions(self):
        if self.action == 'create':  # POST
            return [AllowAny()]
        return [IsAdminUser()]  # GET, PUT, DELETE, etc.

    def create(self, request):
        if CustomUser.objects.filter(username=request.data.get('username')).exists():
            return Response({"message": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(rut=request.data.get('rut')).exists():
            return Response({"message": "RUT already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
