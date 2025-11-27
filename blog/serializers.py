from rest_framework import serializers
from auth_sys.models import MyUser


class MyUserSerialezer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["username", "email", "role", "first_name", "last_name", "birth_date"]

