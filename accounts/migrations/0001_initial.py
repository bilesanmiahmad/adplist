# Generated by Django 4.0.1 on 2022-01-30 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Last Name')),
                ('employer', models.CharField(blank=True, max_length=15, null=True, verbose_name='Employer')),
                ('location', models.CharField(blank=True, max_length=5, null=True, verbose_name='Location')),
                ('title', models.CharField(blank=True, max_length=5, null=True, verbose_name='Title')),
                ('user_type', models.CharField(choices=[('MO', 'Mentor'), ('ME', 'Mentee')], default='ME', max_length=5, verbose_name='User Type')),
                ('expertise', models.CharField(choices=[('UD', 'UI/UX Design'), ('PD', 'Product Design'), ('AD', 'AI Design')], default='UD', max_length=15, verbose_name='Expertise')),
                ('mentor_area', models.CharField(choices=[('CA', 'Career Advice'), ('PR', 'Portfolio Review'), ('IT', 'Interview Techniques'), ('NMA', 'No Mentorship Area')], default='NMA', max_length=15, verbose_name='Mentorship Area')),
                ('is_profile_approved', models.BooleanField(default=False, verbose_name='Is Profile Approved')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
