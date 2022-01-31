from datetime import datetime, timedelta
from django_filters import rest_framework as filters
from django.db.models import Q

from .models import User, Profile


class ProfileFilter(filters.FilterSet):
    user_type = filters.CharFilter(field_name='user_type', lookup_expr='exact')
    is_approved = filters.BooleanFilter(field_name='is_profile_approved', lookup_expr='exact')
    expertise = filters.CharFilter(field_name='expertise', lookup_expr='istartswith')
    delivery_receiver = filters.CharFilter(method='custom_filter')
    since = filters.NumberFilter(method='get_since', lookup_expr='gte')

    class Meta:
        model = Profile
        fields = ["user_type", 'is_approved', 'expertise']
    

