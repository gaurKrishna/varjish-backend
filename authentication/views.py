from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import LoginSerializer, UserSerializer


class SignUpAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        first_name = serializer.validated_data.get("firstname", None)
        last_name = serializer.validated_data.get("lastname", None)
        contact_number = serializer.validated_data.get("contact_number", None)

        if first_name == None:
            return Response({"Error": "First name can not be null"}, status=status.HTTP_400_BAD_REQUEST)

        if last_name == None:
            return Response({"Error": "Last name can not be empty"}, status=status.HTTP_400_BAD_REQUEST)

        if contact_number == None:
            return Response({"Error": "Contact number is required to create your account"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(**serializer.validated_data)
        
        return Response({"status": "User created successfully"}, status=status.HTTP_201_CREATED)


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        print(request.data)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            return Response({"status": "Email id or password incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        token, key = Token.objects.get_or_create(user=user)

        user_data = UserSerializer(user).data

        return Response(
                {
                    "status": "User logged in successfully", 
                    "Token": token.key,
                    "user_details": user_data
                },
                status=status.HTTP_200_OK
            )

    
class LogoutApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            request.user.auth_token.delete()
        except:
            return Response({"status": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST)

        logout(request)

        return Response({"status": "User logged out successfully"}, status=status.HTTP_200_OK)