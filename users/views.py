import logging
from typing import Any, Dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

from main.models import Control
from .models import TUser
from .utils import alert_admin, send_email, logger
from .forms import ContactUsForm
from .paypal_utils import (
    create_paypal_order,
    capture_paypal_order,
    create_paypal_product,
)


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
        if "change_password" in request.POST:
            current_password = request.POST.get("cur_password")
            if user.check_password(current_password):
                new_pass = request.POST.get("password1")
                user.set_password(new_pass)
                user.save()
                messages.success(request, f"User password updated successfuly.")
            else:
                messages.error(request, f"Current passworf is wrong. Update failed")

        return redirect(request.META["HTTP_REFERER"])


class UpgradeView(LoginRequiredMixin, TemplateView):
    """Page for collecting users payment information for upgrading to paid plan"""

    template_name = "users/upgrade.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        amount = request.POST.get("amount")
        currency = "USD"
        return_url = request.build_absolute_uri(reverse("users:execute-payment"))
        cancel_url = request.build_absolute_uri(reverse("users:cancel-payment"))

        try:
            order = create_paypal_order(
                request, amount, currency, return_url, cancel_url
            )
            approval_url = None
            for link in order["links"]:
                if link["rel"] == "approve":
                    approval_url = link["href"]
                    user.balance += float(amount)
                    user.save()
            return JsonResponse({"url": approval_url}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Error creating the payment"}, status=400)


class PayPalSettingsView(LoginRequiredMixin, TemplateView):
    """Paypal settings view"""

    template_name = "users/paypal_settings.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, **kwargs):
        if "create_product" in request.POST:
            name = request.POST.get("product_name")
            # price = request.POST.get("price")
            # currency = request.POST.get("currency")
            try:
                product = Control.objects.create(
                    name="paypal_product", json_value=create_paypal_product(name)
                )

                messages.success(
                    request, f"Paypal product {product} created successfuly."
                )
            except Exception as e:
                logger.error(e)
                messages.error(request, f"Error creating the product. Error: {e}")
        return redirect(request.META["HTTP_REFERER"])


@login_required
def execute_payment(request):
    token = request.GET.get("token", None)
    payer_id = request.GET.get("PayerID", None)
    response_data = {"status": "error"}

    if token and payer_id:
        try:
            capture_paypal_order(token)
            return redirect(f"{reverse('users:upgrade')}?payment_status=success")
        except Exception as e:
            logger.error(e)
            return redirect(f"{reverse('users:upgrade')}?payment_status=error")
    else:
        return redirect(f"{reverse('users:upgrade')}?payment_status=invalid")


def cancel_payment(request):
    return HttpResponse("Payment canceled.")


class ContactUs(LoginRequiredMixin, FormView):
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
