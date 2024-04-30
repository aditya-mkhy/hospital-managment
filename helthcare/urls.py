from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    path("login", view=views.login_user, name="login"),
    path("logout", view=views.logout_user, name="logout"),
    path("signup", view=views.signupuser, name="signup"),
    path("contact", view=views.forgot, name="contact"),
    path("forgot", view=views.forgot, name="forgot"),
    path("test", view=views.test_page, name="test"),
    path("profile", view=views.profile_img, name="/profile"),
]