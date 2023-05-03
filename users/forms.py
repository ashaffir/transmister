from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC

from users.utils import alert_admin, EmailThread
from main.models import Control
from .models import TUser, ContactUs

User = get_user_model()


class ContactUsForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    subject = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = ContactUs
        exclude = ("created",)


class TUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    password1: forms.Field
    password2: forms.Field
    team_member = forms.BooleanField(required=False)

    class Meta:
        model = TUser
        fields = (
            "email",
            "team_member",
        )

        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
            "team_member": forms.CheckboxInput(attrs={"class": "form-control"}),
        }


class TUserSignupForm(SignupForm):
    def clean_email(self):
        email = self.cleaned_data.get("email")

        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError(
                "A user with this email address already exists."
            )

        return email

    def save(self, request):
        user = super(TUserSignupForm, self).save(request)

        if user is None:
            return user

        init_balance, created = Control.objects.get_or_create(name="balance")

        if created:
            init_balance.float_value = 0.075
            init_balance.save()

        user.balance = init_balance.float_value
        user.save()

        context = {}

        title = f"New signup"

        context["message"] = {
            "email_type": "new_user_signup",
            "user": user,
            "email": user.email,
            "type": "Customer",
        }

        alert_admin(title=title, message=None, context=context)

        return user


class TUserChangeForm(UserChangeForm):
    class Meta:
        model = TUser
        fields = ("username", "email")
