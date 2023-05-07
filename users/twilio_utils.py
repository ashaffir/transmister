from twilio.rest import Client
from django.conf import settings

# Read more at http://twil.io/secure
account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
verify_sid = settings.TWILIO_VERIFY_SID

client = Client(account_sid, auth_token)


def send_otp(phone_number):
    verification = client.verify.v2.services(verify_sid).verifications.create(
        to=phone_number, channel="sms"
    )
    print(verification.status)


def verify_otp(phone_number, otp):
    print(f"{1}")
    verification_check = client.verify.v2.services(
        verify_sid
    ).verification_checks.create(to=phone_number, code=otp)
    print(f"{2}")
    return verification_check.status
