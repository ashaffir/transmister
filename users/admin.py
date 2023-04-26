from django.contrib import admin
from .models import ContactUs, TUser


@admin.register(TUser)
class TUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "joined",
        "email",
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
        "email",
        "subject",
        "message",
    )
    search_fields = (
        "email",
        "subject",
        "message",
    )
    ordering = ("-created",)
