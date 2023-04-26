from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView


from . import views


app_name = "users"


urlpatterns = [
    #   path("", views.Home.as_view(), name="home"),
    path("contact-us/", views.ContactUs.as_view(), name="contact-us"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "forgot-password/", views.ForgotPasswordView.as_view(), name="forgot-password"
    ),
]
