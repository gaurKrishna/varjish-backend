from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["firstname", "lastname", "email", "password", "role", "contact_number", "profile"]
        read_only_fields = ("profile")

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=68, min_length=7)
    
    class Meta:
        fields = ["eamil", "password"]