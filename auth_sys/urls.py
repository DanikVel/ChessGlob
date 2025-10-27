from django.urls import path
import auth_sys.views as views

urlpatterns = [path("login", views.login_user, name="login"),
               path("register", views.register_user, name="register")]

app_name = "auth_sys"
