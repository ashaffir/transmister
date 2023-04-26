import threading
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import loader
from allauth.account.adapter import DefaultAccountAdapter


class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, html_email=None):
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.html_email = html_email
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(
            self.subject, self.body, self.from_email, self.recipient_list
        )
        if self.html_email:
            msg.attach_alternative(self.html_email, "text/html")
        msg.send()


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        subject = loader.render_to_string(f"{template_prefix}_subject.txt", context)
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(f"{template_prefix}_message.txt", context)
        html_email = loader.render_to_string(f"{template_prefix}_message.html", context)

        EmailThread(
            subject, body, settings.DEFAULT_FROM_EMAIL, [email], html_email
        ).start()
