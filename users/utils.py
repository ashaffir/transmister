from concurrent.futures import thread
import logging
import threading
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.template import RequestContext, TemplateDoesNotExist

from main.models import Control

logger = logging.getLogger(__file__)


class EmailThread(threading.Thread):
    """Sending an email in a thread"""

    def __init__(
        self, email, title, message, from_email, html_email_template_name, context
    ) -> None:
        self.email = email
        self.title = title
        self.messae = message
        self.from_email = from_email
        self.html_email_template_name = html_email_template_name
        self.context = context
        threading.Thread.__init__(self)

    def run(self):
        logger.info(f"start threading sending to {self.email}")
        try:
            send_email(
                title=self.title,
                email_template_name=None,
                context=self.context,
                html_email_template_name=self.html_email_template_name,
                request=None,
                mail_list=self.email,
            )
            logger.info("------- send complete -----------")
        except Exception as e:
            logger.info(f"ERROR: {e}")


def send_email(
    title,
    email_template_name,
    context,
    html_email_template_name=None,
    request=None,
    mail_list=[],
) -> None:
    """Send an email"""
    subject = title
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = mail_list
    logger.info(f"send to {to_email}")
    ctx_dict = {}
    if request is not None:
        ctx_dict = RequestContext(request, ctx_dict)

    if context:
        ctx_dict.update(context)

    # Email subject *must not* contain newlines
    from_email = from_email or getattr(settings, "DEFAULT_FROM_EMAIL")
    if email_template_name:
        message_txt = render_to_string(email_template_name, ctx_dict)

        email_message = EmailMultiAlternatives(
            subject, message_txt, from_email, to_email
        )
    else:
        try:
            message_html = render_to_string(html_email_template_name, ctx_dict)
            email_message = EmailMultiAlternatives(
                subject, message_html, from_email, to_email
            )
            email_message.content_subtype = "html"
        except TemplateDoesNotExist:
            pass
    try:
        email_message.send()
        logger.info(f"<MLO>> Email sent successfully.")
    except Exception as e:
        logger.error(f"Email not sent. Reason: {e}")


def alert_admin(title, message, context=None, mail_list=[]) -> None:
    """Send a message to admin


    Args:
      alert (str): The message
    """

    logger.info(f">>> Alerting Admin <<<")
    subject = title
    message_txt = message
    from_email = settings.DEFAULT_FROM_EMAIL

    admin_mail_list, created = Control.objects.get_or_create(name="admin_mail_list")
    if created:
        admin_mail_list.json_value = [settings.ADMIN_EMAIL]
        admin_mail_list.save()

    to_email = admin_mail_list.json_value
    context = context
    email_message = EmailThread(
        email=to_email,
        title=subject,
        message=message_txt,
        from_email=from_email,
        html_email_template_name="main/emails/admin_email.html",
        context=context,
    )
    try:
        email_message.start()
        logger.info(f"<MLO>> Alert email sent successfully.")
    except Exception as e:
        logger.error(f"ERROR: email not sent (utilities.py). Reason: {e}")
