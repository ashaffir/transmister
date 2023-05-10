from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm

from users.utils import alert_admin, EmailThread
from main.models import Control
from transmister.settings import PRICE_PER_MINUTE
from .models import TUser, ContactUs


User = get_user_model()


class ContactUsForm(forms.ModelForm):
    subject = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = ContactUs
        fields = ("subject", "message")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(ContactUsForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ContactUsForm, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance


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
            init_balance.float_value = PRICE_PER_MINUTE * 5
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


class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={"class": "form-control"})
    )


class PhoneNumberVerificationForm(forms.Form):
    verification_code = forms.CharField(
        max_length=5, widget=forms.TextInput(attrs={"class": "form-control"})
    )
