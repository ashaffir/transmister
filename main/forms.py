from django import forms
from .models import Recording


class RecordingForm(forms.ModelForm):
    language = forms.CharField(required=False)

    class Meta:
        model = Recording
        fields = (
            "session",
            "voice_recording",
            "audio_type",
            "language",
        )
