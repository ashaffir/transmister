import subprocess
import openai
import logging
from pydub import AudioSegment
from django.core.mail import EmailMultiAlternatives

from django.core.mail import send_mail
from django.conf import settings

from transmister.settings import OPENAI_KEY

logger = logging.getLogger(__file__)


def alert_admin(alert):
    """Send a message to admin

    Args:
        alert (str): The message
    """
    subject = "Toromate Alert"
    message_txt = alert
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [settings.ADMIN_EMAIL]
    email_message = EmailMultiAlternatives(subject, message_txt, from_email, to_email)
    try:
        email_message.send()
    except Exception as e:
        logger.error(f"ERROR: email not sent (utilities.py). Reason: {e}")

    logger.info(f">>> Alerting Admin <<<")


openai.api_key = OPENAI_KEY


def transcribe_api(audio_file, language: str = "he"):
    audio_file = open(audio_file, "rb")
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file, language=language)
    except Exception as e:
        logger.error(f"Error transcribing audio file: {e}")
        alert_admin(f"Error transcribing audio file: {e}")
        raise e

    user_text = f"{transcript['text']}"

    return user_text


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
            output_file,
        ]
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting audio file: {e}")
        return False


def calculate_audio_duration(audio_file):
    """Calculating the duration of the audio for the transcription"""
    audio = AudioSegment.from_file(audio_file)
    duration_ms = len(audio)
    duration_s = duration_ms / 1000
    duration_min = duration_s / 60
    return duration_min


def get_recording_duration(file_name: str) -> float:
    """Get the duration of the recording"""
    from main.models import Recording

    try:
        recording_id = file_name.split("/")[-1].split(".")[-2]
        recording = Recording.objects.get(id=recording_id)
        return recording.duration
    except:
        recording_id = file_name.split("/")[-1].split("_")[-2]
        recording = Recording.objects.get(id=recording_id)
        return recording.duration
