from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import CustomUser
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from django.contrib.auth import get_user_model
User=get_user_model()


p1=RegexValidator(r'^(?=.*[A-Z])(?=.*[!@#$%^&*()])(.{8,})$','min 8 charectors')

# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Student
#         fields=['id','name','age','place']


class Userserializers(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,validators=[p1])
    email=serializers.EmailField(required=True)
    def create(self, validated_data):
        user=CustomUser.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model=CustomUser
        fields=['username','password','email']


        extra_kwargs = {
            'email': {
                'required': True,
                'validators': [UniqueValidator(queryset=User.objects.all())]
            }
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

# class ResetPasswordEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)