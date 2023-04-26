from typing import Iterable, Optional
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from ckeditor.fields import RichTextField


class TUser(AbstractUser):
    """Custom user model"""

    joined = models.DateTimeField(auto_now_add=True)
    team = models.CharField(max_length=100, blank=True, null=True)
    categories_of_interest = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = "T User"
        verbose_name_plural = "T Users"

    def __str__(self) -> str:
        return f"{self.email}"


class ContactUs(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    email = models.EmailField()
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
