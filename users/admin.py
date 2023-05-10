from django.contrib import admin
from .models import ContactUs, TUser


@admin.register(TUser)
class TUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "joined",
        "email",
        "balance",
        "is_active",
    )
    search_fields = (
        "username",
        "email",
    )
    ordering = ("-joined",)


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subject",
        "message",
    )
    search_fields = (
        "user",
        "subject",
        "message",
    )
    ordering = ("-created",)
