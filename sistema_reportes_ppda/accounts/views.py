from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    

class RegisterUserAPIView(APIView):
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
