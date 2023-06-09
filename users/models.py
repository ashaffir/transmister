import uuid
from typing import Iterable, Optional
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.conf import settings


class TUser(AbstractUser):
    """Custom user model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    joined = models.DateTimeField(auto_now_add=True)
    team = models.CharField(max_length=100, blank=True, null=True)
    categories_of_interest = models.JSONField(default=list, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    phone_number_verified = models.BooleanField(default=False)
    balance = models.FloatField(default=0.075)
    twilio_send_again_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "T User"
        verbose_name_plural = "T Users"

    def __str__(self) -> str:
        return f"{self.email}"

    def get_available_minutes(self):
        """Return the number of minutes available for this user"""
        return self.balance / settings.PRICE_PER_MINUTE

    def get_transcriptions_count(self):
        """Return the number of transcriptions this user has made"""
        from main.models import Transcription

        return Transcription.objects.filter(user=self).count()

    def get_total_transactions_duration(self):
        """Return the total duration of all transactions this user has made"""
        from main.models import Transcription

        total_duration_min = Transcription.objects.filter(user=self).aggregate(
            models.Sum("duration")
        )["duration__sum"]

        if total_duration_min is None:
            return 0
        else:
            return round(total_duration_min, 3)


class ContactUs(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(TUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __str__(self) -> str:
        return f"{self.name}"


class PageItems(models.Model):
    """Text times on the home page for admin side edits"""

    page = models.CharField(max_length=20)
    section = models.CharField(max_length=20)
    sub_section = models.CharField(max_length=20)

    title = models.CharField(max_length=50)
    content = RichTextField()

    class Meta:
        verbose_name = "Homepage item"
        verbose_name_plural = "Homepage items"
