from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.db import IntegrityError
from .models import CustomUser
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from django.contrib.auth import get_user_model
# CustomUser=get_user_model()
from .validators import validate_password_complexity,validate_email,validate_username

#p1=RegexValidator(r'^(?=.*[A-Z])(?=.*[!@#$%^&*()])(.{8,})$','min 8 charectors')




class Userserializers(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,validators=[validate_password_complexity])
    email=serializers.EmailField(required=True,validators=[validate_email])
    username=serializers.CharField(required=True,validators=[validate_username])
    class Meta:
        model=CustomUser
        fields=['username','email','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user=CustomUser.objects.create(username=validated_data['username'],email=validated_data['email'])
            user.set_password(validated_data['password'])
            user.save()
            return user
        except :
            raise serializers.ValidationError({"error": "Username or email already exists."})



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

# class ResetPasswordEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)