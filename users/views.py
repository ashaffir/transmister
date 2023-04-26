import logging
from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from .models import TUser
from .utils import alert_admin, send_email, logger
from .forms import ContactUsForm


class Home(TemplateView):
    """User homepage"""

    template_name = "users/home.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "home"
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile view"""

    template_name: str = "users/profile.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request):
        user = request.user
        if "add_category" in request.POST:
            new_category = request.POST.get("categories_select")
            if new_category not in request.user.categories_of_interest:
                request.user.categories_of_interest.append(new_category)
            request.user.save()
        elif "delete_category" in request.POST:
            category_to_delete = request.POST.get(f"user_category")
            request.user.categories_of_interest.remove(category_to_delete)
            request.user.save()
        elif "update_personals" in request.POST:
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.team = request.POST.get("team")
            user.save()
            messages.success(request, f"User data updated successfuly.")
        elif "update_password" in request.POST:
            current_password = request.POST.get("cur_password")
            if user.check_password(current_password):
                new_pass = request.POST.get("password1")
                user.set_password(new_pass)
                user.save()
                messages.success(request, f"User password updated successfuly.")
            else:
                messages.error(request, f"Current passworf is wrong. Update failed")

        return redirect(request.META["HTTP_REFERER"])


class ContactUs(FormView):
    """Contact us page"""

    form_class = ContactUsForm
    template_name = "users/contact_us.html"
    success_url = "/"

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
            title = f"Contact us message from {request.user}"
            context = {}
            context["message"] = {
                "email_type": "contact_us",
                "user": request.user,
                "subject": subject,
                "message": message,
            }
            alert_admin(title=title, message=message, context=context)
            logging.info(f"<MLO>> Contact us message sent from {request.user}")
            messages.success(
                request, "Your message has been sent. We'll get back to you shortly"
            )
            return redirect(request.META["HTTP_REFERER"])
        else:
            logging.error(f"<MLO>> Contact us failed")
            return redirect(request.META["HTTP_REFERER"])


class ForgotPasswordView(TemplateView):
    """Handling forgot-password situations"""

    template_name: str = "account/forgot_password.html"

    def post(self, request):
        email = request.POST.get("email")
        if email:
            if "@" in email:
                user = TUser.objects.filter(email=email).first()
                logger.info(f"User {user} forgot password")
                if user is not None:
                    token_generator = default_token_generator

                    context = {
                        "domain": request._current_scheme_host,
                        "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": token_generator.make_token(user),
                        "user": user,
                    }

                    try:
                        send_email(
                            "Reset Password",
                            email_template_name=None,
                            context=context,
                            mail_list=[email],
                            html_email_template_name="account/emails/change_password_email.html",
                        )
                    except Exception as e:
                        alert_admin(title="Error seding email", message=f"{e}")
                        logger.error(f"Email configurations error: {e}")

        messages.success(
            request, "If this email is in our system you will receive instructions."
        )
        return redirect("account_login")
