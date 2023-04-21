from django.contrib import admin

from main.models import Recording, Transcription, RecodringSession, Control


@admin.register(Recording)
class RecordAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created",
        "language",
    ]
    ordering = ["-created"]


@admin.register(Transcription)
class TranscriptioAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created",
        "file",
        "language",
    ]
    ordering = ("-created",)


@admin.register(RecodringSession)
class RecordingSessionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "started",
        "ended",
    ]
    ordering = ("-started",)


@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "int_value",
        "float_value",
        "bool_value",
        "json_value",
        "string_value",
    ]
    search_fields = [
        "name",
        "string_value",
    ]
