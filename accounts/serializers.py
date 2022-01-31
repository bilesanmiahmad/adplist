from logging.config import valid_ident
from rest_framework import serializers
from .models import User, Profile


MENTOR = 'MO'
MEMBER = 'ME'
UIUX = 'UD'
PRODUCT_DESIGN = 'PD'
AI_DESIGN = 'AD'
CAREER_ADVICE = 'CA'
PORTFOLIO_REVIEW = 'PR'
INTERVIEW_TECHNIQUES = 'IT'
NO_MENTOR_AREA = 'NMA'

USER_TYPES = (
    (MENTOR, 'Mentor'),
    (MEMBER, 'Mentee'),
)

EXPERTISE = (
    (UIUX, 'UI/UX Design'),
    (PRODUCT_DESIGN, 'Product Design'),
    (AI_DESIGN, 'AI Design')
)

MENTOR_AREA = (
    (CAREER_ADVICE, 'Career Advice'),
    (PORTFOLIO_REVIEW, 'Portfolio Review'),
    (INTERVIEW_TECHNIQUES, 'Interview Techniques'),
    (NO_MENTOR_AREA, 'No Mentorship Area')
)


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


class ProfileCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    employer = serializers.CharField(required=True, write_only=True)
    location = serializers.CharField(required=True, write_only=True)
    title = serializers.CharField(required=True, write_only=True)
    user_type = serializers.ChoiceField(required=True, write_only=True, choices=USER_TYPES)
    expertise = serializers.ChoiceField(required=True, write_only=True, choices=EXPERTISE)
    mentor_area = serializers.ChoiceField(required=True, write_only=True, choices=MENTOR_AREA)

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('A profile requires a user')
        profile = Profile.objects.get(user=user)
        profile.first_name = validated_data['first_name']
        profile.last_name = validated_data['last_name']
        profile.employer = validated_data['employer']
        profile.location = validated_data['location']
        profile.title = validated_data['title']
        profile.user_type = validated_data['user_type']
        profile.expertise = validated_data['expertise']
        profile.mentor_area = validated_data['mentor_area']

        if profile.user_type == 'ME':
            profile.mentor_area = 'NMA'
        profile.save()
        return profile


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
