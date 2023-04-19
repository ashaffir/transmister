import os
import subprocess
import uuid
from datetime import datetime
from django.db import models
from django.urls.base import reverse
from django.core.files.base import ContentFile

from .utils import logger


def recording_path(instance, filename):
    return f"recordings/{instance.session}/{instance.pk}.wav"


class Recording(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    session = models.CharField(max_length=100)
    voice_recording = models.FileField(upload_to=recording_path)
    audio_type = models.CharField(max_length=50)
    language = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Check the file type
        input_file = self.voice_recording.path
        logger.info(f"{self.audio_type=}")
        if "aac" in self.audio_type or "mp4" in self.audio_type:
            output_file = os.path.splitext(input_file)[0] + "_conv.wav"

            if self.convert_aac_to_wav(input_file, output_file):
                with open(output_file, "rb") as converted_file:
                    content = ContentFile(converted_file.read())
                    self.voice_recording.save(
                        os.path.basename(output_file), content, save=False
                    )
                    os.remove(output_file)  # Remove the temporary WAV file

                os.remove(input_file)  # Remove the original AAC file
                super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __str__(self):
        return str(self.id)

    @staticmethod
    def convert_aac_to_wav(input_file, output_file):
        try:
            ffmpeg_path = "ffmpeg"  # Adjust this if FFmpeg is not in your system's PATH
            cmd = [
                ffmpeg_path,
                "-i",
                input_file,
                "-acodec",
                "pcm_s16le",
                "-ar",
                "16000",
                "-ac",
                "1",
                "-y",
                output_file,
            ]
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error converting audio file: {e}")
            return False

    def get_absolute_url(self):
        return reverse("main:record_detail", kwargs={"id": str(self.id)})


class Transcription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    session = models.CharField(max_length=100)
    file = models.FileField()
    language = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Transcription"
        verbose_name_plural = "Transcriptions"

    def __str__(self):
        return str(self.id)

    def get_file_name(self):
        return self.file.name.split("/")[-1]

    def get_content(self):
        with open(self.file.name, "r") as f:
            content = f.readlines()
        return content


class RecodringSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    started = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(null=True, blank=True)
    recordings = models.JSONField(default=list)
    transcription = models.ForeignKey(
        Transcription, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Recording Session"
        verbose_name_plural = "Recording Sessions"

    def __str__(self):
        return str(self.id)

    def get_current_count(self):
        return len(self.recordings)
