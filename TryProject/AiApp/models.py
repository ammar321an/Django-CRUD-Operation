from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RegistrationForm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    repassword = models.CharField(max_length=128)
    date_reg = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'registration_form'