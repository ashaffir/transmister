from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect


class PhoneNumberVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.verify_phone_number(request)
        return response

    def verify_phone_number(self, request):
        user = request.user

        if (
            user.is_authenticated
            and not user.is_superuser
            and not user.phone_number_verified
        ):
            # List of URLs that don't require phone number verification
            if user.phone_number:
                allowed_urls = [
                    "/users/verify-phone-number/",
                    "/users/resend-otp/",
                    "/logout/",
                ]
                if request.path not in allowed_urls:
                    return redirect(reverse("users:verify-phone-number"))
            else:
                allowed_urls = [
                    "/users/submit-phone-number/",
                    "/logout/",
                ]
                if request.path not in allowed_urls:
                    return redirect(reverse("users:submit-phone-number"))

        return self.get_response(request)
