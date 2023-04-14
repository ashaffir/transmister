import os
import glob
from datetime import datetime
from typing import Any, Dict
from django.views.generic import TemplateView
from django.views import View
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from transmister.settings import MEDIA_ROOT, MEDIA_URL
from .models import Recording, Transcription
from .utils import convert_aac_to_wav, transcribe, logger


@method_decorator(csrf_exempt, name="dispatch")
class HomeView(TemplateView):
    """Home page"""

    template_name = "main/recording.html"

    def get(self, request):
        context = {}
        try:
            session_id = request.session["session"]
            session_path = f"{MEDIA_ROOT}/recordings/{request.session['session']}"
            if glob.glob(f"{session_path}/transcript_{session_id}.txt"):
                with open(
                    f"{session_path}/transcript_{session_id}.txt", "r"
                ) as txt_file:
                    context["transcription"] = txt_file.read()
        except:
            logger.warning("no session ID exising. setting a new one")

        # Setting a new session ID (timestamp) for the files path
        request.session["session"] = int(datetime.timestamp(datetime.now()))
        return render(request, self.template_name, context=context)

    def post(self, request):
        session_id = request.session["session"]
        session_path = f"{MEDIA_ROOT}/recordings/{session_id}"
        files = sorted(glob.glob(f"{session_path}/*.wav"), key=os.path.getmtime)
        if len(files) > 0:
            transcription_file = f"{session_path}/transcript_{session_id}.txt"
            with open(transcription_file, "a") as txt_file:
                for idx, file in enumerate(files, start=1):
                    try:
                        txt = transcribe(file)
                    except Exception as e:
                        logger.error(f"<ALS>> Transcribe error: {e}")
                        messages.error(f"{e}")

                    txt_file.writelines(f"{idx}- {txt}\n")
            Transcription.objects.create(file=transcription_file, session=session_id)

        else:
            messages.warning(request, "No files to transcribe")
        return redirect(request.META["HTTP_REFERER"])


class UserTranscriptionsView(TemplateView):
    """List of all current recordings that the user has"""

    template_name = "main/user_transcriptions.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["media_url"] = f"{MEDIA_URL}recordings"
        context["transcs"] = Transcription.objects.all()
        return context


@csrf_exempt
def upload_audio(request):
    try:
        audio_blob = request.FILES["audio_blob"]
        device = request.POST["device"]
        recording = Recording(
            session=request.session["session"],
            voice_recording=audio_blob,
            audio_type=device,
        )
        recording.save()

        return JsonResponse({"success": True})
    except Exception as e:
        logger.error(f"<ALS>> Failed uploading audio: {e}")
        return JsonResponse({"success": False})
