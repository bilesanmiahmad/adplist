from logging.config import valid_ident
from rest_framework import serializers
from .models import User, Profile


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        profile = Profile(user=user)
        profile.save() 
        return user
    
    def validate_email(self, value):
        val_email = value.lower()
        try:
            User.objects.get(email=val_email)
            raise serializers.ValidationError('User already exists')
        except User.DoesNotExist:
            return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'date_joined']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'first_name', 'last_name', 'employer', 'title', 'expertise', 
        'mentor_area', 'location', 'user_type', 'is_profile_approved', 'date_created', 'date_updated']

class FullUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['email', 'date_joined', 'auth_token', 'profile']
