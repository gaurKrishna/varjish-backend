from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["firstname", "lastname", "email", "password", "role", "contact_number"]

class LoginSerializer(serializers.Serializer):
    eamil = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=68, min_length=7)
    
    class Meta:
        fields = ["eamil", "password"]