from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin



class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username: raise ValueError("Користувач повинен мати юзернейм!")
        if not email: raise ValueError("Користувач повинен мати почту!")

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices): #Усі можливі ролі
        USER = "user"
        ADMINISTRATOR = "administrator"
    #Обов'язкові данні
    username = models.CharField(unique=True, max_length=16)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=Roles.choices, default=Roles.USER)
    #Необов'язкові данні, які користувач буде додавати по власному бажанню
    first_name = models.CharField(blank=True, null=True, max_length=16)
    last_name = models.CharField(blank=True, null=True, max_length=32)
    birth_date = models.DateField(blank=True, null=True)
    
    #Данні потрібні для Django адмінки
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager() #Це потрібно для створення самого акаунту
    #Оголошую, що username - головне поле для логіну
    USERNAME_FIELD = "username"
    #Вказую обов'язкові поля при створенні юзера
    REQUIRED_FIELDS = ["email"]

    def __str__(self): return f"{self.role} | {self.username} - {self.email}"

