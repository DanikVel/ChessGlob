from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import auth_sys.models as models



@admin.register(models.MyUser) #Регістрація моделі юзера
class MyUserAdmin(UserAdmin):
    model = models.MyUser

    #Змінні для колонки користувачів в адмін панелі
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    #Як групуються поля при редагуванні користувача
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Персональна інформація", {"fields": ("first_name", "last_name", "birth_date")}),
        ("Ролі та права", {"fields": ("role", "is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Інше", {"fields": ("last_login",)}))

    #Поля при створенні користувача
    add_fieldsets = (
        (None, {"classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "is_staff", "is_active")}))
    
    search_fields = ("username", "email")
    ordering = ("username",)

