from rest_framework import generics, views, status
from .models import CustomUser
from rest_framework.response import Response
from .serializers import CustomUserSerializer, LoginSerializer
from django.contrib.auth import authenticate, login
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return user
    

class LoginView(views.APIView):
    
    serialiazer_class = LoginSerializer
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
        ),
        responses={200: 'Login successful', 401: 'Invalid credentials'},
    )
    
    def post(self, request, *args, **kwargs):
        serializer = self.serialiazer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user and user.is_active():
            login(request, user)
            return Response({"user": user.id, "message": "Welcome, you've logged in successfully."})
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

