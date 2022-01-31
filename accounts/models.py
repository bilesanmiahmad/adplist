from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser

from rest_framework.authtoken.models import Token


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates a new user
        """
        if not email:
            raise ValueError("This object requires an email")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        Token.objects.get_or_create(user=user)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'Email Address',
        unique=True
    )
    
    date_joined = models.DateTimeField(
        'Date Joined',
        auto_now_add=True
    )
    is_active = models.BooleanField(
        'Active',
        default=True
    )
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def get_full_name(self):
        full_name = f'{self.email}'
        return full_name
    
    def get_short_name(self):
        return self.email
    
    def __str__(self):
        return self.email


class Profile(models.Model):
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

    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        related_name='profile'
    )
    first_name = models.CharField(
        'First Name',
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        'Last Name',
        max_length=30,
        blank=True
    )
    employer = models.CharField(
        'Employer',
        max_length=15,
        blank=True,
        null=True
    )
    location = models.CharField(
        'Location',
        max_length=5,
        blank=True,
        null=True
    )
    title = models.CharField(
        'Title',
        max_length=5,
        blank=True,
        null=True
    )
    user_type = models.CharField(
        'User Type',
        max_length=5,
        choices=USER_TYPES,
        default=MEMBER
    )
    expertise = models.CharField(
        'Expertise',
        max_length=15,
        choices=EXPERTISE,
        default=UIUX
    )
    mentor_area = models.CharField(
        'Mentorship Area',
        max_length=15,
        choices=MENTOR_AREA,
        default=NO_MENTOR_AREA
    )

    is_profile_approved = models.BooleanField(
        'Is Profile Approved',
        default=False
    )
    
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email