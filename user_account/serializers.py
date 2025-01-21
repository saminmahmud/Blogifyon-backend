from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from author.models import Author
import requests
from django.conf import settings
User = get_user_model()

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    recaptcha_token = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'recaptcha_token')

    def validate(self, data):
        # Verify the reCAPTCHA token
        recaptcha_token = data.get('recaptcha_token')
        recaptcha_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_token
            }
        )
        recaptcha_result = recaptcha_response.json()
        if not recaptcha_result.get('success'):
            raise serializers.ValidationError("reCAPTCHA validation failed.")

        # check password and confirm password 
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")
        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False,
        )
        user_account = Author.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)
    recaptcha_token = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        recaptcha_token = data.get('recaptcha_token')
        
        # Verify the reCAPTCHA token
        recaptcha_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_token
            }
        )
        recaptcha_result = recaptcha_response.json()
        if not recaptcha_result.get('success'):
            raise serializers.ValidationError("reCAPTCHA validation failed.")

        # Authenticate user
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("This account is inactive.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
        print("serializing done.")
        return data
