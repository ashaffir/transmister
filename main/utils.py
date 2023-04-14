import os
import subprocess
import openai
import logging
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
        print(f"email not sent. ERROR: {e}")

    print(f">>> Alerting Admin <<<")
    logger.info(f">>> Alerting Admin <<<")


openai.api_key = OPENAI_KEY


def transcribe(audio_file):
    audio_file = open(audio_file, "rb")
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file, language="he")
    except Exception as e:
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
        print(f"Error converting audio file: {e}")
        return False
