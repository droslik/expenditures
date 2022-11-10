from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    is_income = models.BooleanField(default=False)
    is_basic = models.BooleanField(default=False)


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        ADMIN = 'admin'
    role = models.CharField(max_length=9, choices=Roles.choices)
    categories = models.ManyToManyField(Category, related_name="users")


class Account(models.Model):
    number = models.CharField(unique=True, max_length=13)
    amount = models.IntegerField(default=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')


class Transaction(models.Model):
    amount = models.IntegerField(name=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories')
    organization = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    transaction_date = models.DateTimeField(default=timezone.now)
