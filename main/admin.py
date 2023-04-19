from django.contrib import admin

from main.models import Recording, Transcription, RecodringSession


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
