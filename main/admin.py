from django.contrib import admin

from main.models import Recording, Transcription, RecodringSession, Control


@admin.register(Recording)
class RecordAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created",
        "user",
        "duration",
    ]
    ordering = ["-created"]


@admin.register(Transcription)
class TranscriptioAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created",
        "user",
        "language",
    ]
    search_fields = [
        "file",
    ]
    ordering = ("-created",)


@admin.register(RecodringSession)
class RecordingSessionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "started",
        "ended",
    ]
    ordering = ("-ended",)


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
