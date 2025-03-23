from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from custom_permissions import IsSMAOrSelf, IsSMAUser

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
            return [IsSMAUser()]  # Solo SMA puede ver la lista

        if self.action in ["update", "partial_update", "retrieve", "destroy"]:
            return [IsSMAOrSelf()]  # SMA puede hacer todo, otros solo su perfil

        return super().get_permissions()
    

class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]  # By default all endpoints require Auth, but registration should be public?
    def post(self, request):
        
        if CustomUser.objects.filter(username=request.data.get('username')).exists():
            return Response({"message": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(rut=request.data.get('rut')).exists():
            return Response({"message": "RUT already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
