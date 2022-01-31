from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from accounts import serializers

from accounts.models import User, Profile
from accounts.serializers import UserSerializer, SignupSerializer, FullUserSerializer, ProfileSerializer

from accounts.filters import ProfileFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post'], detail=False, url_path='signup', permission_classes=[AllowAny])
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                Token.objects.create(user=user)
                user.save()
                user_serializer = UserSerializer(user)
            return Response(
                {
                    'results': user_serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'errors': serializer.errors
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    @action(methods=['post'], detail=False, url_path='login', permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user:
            serializer = FullUserSerializer(user)
            return Response(
                {
                    'results': serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'errors': 'User email or password is wrong'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter

    @action(methods=['put'], detail=False, url_path='complete-profile', permission_classes=[IsAuthenticated])
    def complete_profile(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        profile.first_name = request.data.get('first_name')
        profile.last_name = request.data.get('last_name')
        profile.employer = request.data.get('employer')
        profile.location = request.data.get('location')
        profile.title = request.data.get('title')
        profile.user_type = request.data.get('user_type')
        profile.expertise = request.data.get('expertise')
        profile.mentor_area = request.data.get('mentor_area')
        if profile.user_type == 'ME':
            profile.mentor_area = 'NMA'
            profile.is_profile_approved = True
        profile.save()
        serializer = FullUserSerializer(user)
        return Response(
            {
                'results': serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(methods=['patch'], detail=False, url_path='approve-profile', permission_classes=[IsAdminUser])
    def approve_profile(self, request):
        user_email = request.data.get('email')
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response(
                {
                    'error': f'User with email {user_email} does not exist'
                }
            )
        user_profile = Profile.objects.get(user=user)
        if user_profile.user_type == 'ME':
            return Response(
                {
                    'error': 'Members do not require approval'
                }
            )
        user_profile.is_profile_approved = True
        user_profile.save()
        serializer = FullUserSerializer(user)
        return Response(
            {
                'results': serializer.data
            },
            status=status.HTTP_200_OK
        )
    