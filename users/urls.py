from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView


from . import views


app_name = "users"


urlpatterns = [
    #   path("", views.Home.as_view(), name="home"),
    path("contact-us/", views.ContactUs.as_view(), name="contact-us"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("upgrade/", views.UpgradeView.as_view(), name="upgrade"),
    path(
        "paypal-settings/", views.PayPalSettingsView.as_view(), name="paypal-settings"
    ),
    path("execute-payment/", views.execute_payment, name="execute-payment"),
    path("cancel-payment/", views.cancel_payment, name="cancel-payment"),
    path(
        "forgot-password/", views.ForgotPasswordView.as_view(), name="forgot-password"
    ),
]
