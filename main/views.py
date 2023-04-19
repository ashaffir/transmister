import os
import glob
from datetime import datetime
from typing import Any, Dict
from django.views.generic import TemplateView
from django.views import View
from django.utils.timezone import make_aware
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from transmister.settings import MEDIA_ROOT, MEDIA_URL
from .models import RecodringSession, Recording, Transcription
from .utils import convert_aac_to_wav, transcribe_api, logger


class HomeView(TemplateView):
    """Home page"""

    template_name = "main/recording.html"

    def get(self, request):
        context = {}
        # Getting the last open session
        curr_session = RecodringSession.objects.filter(ended__isnull=True).last()
        if not curr_session:
            curr_session = RecodringSession.objects.create()

        context["session"] = curr_session
        context["recordings"] = Recording.objects.filter(session=curr_session.id)

        # try:
        #     session_path = f"{MEDIA_ROOT}/recordings/{curr_session.id}"
        #     if glob.glob(f"{session_path}/transcript_{curr_session.id}.txt"):
        #         with open(
        #             f"{session_path}/transcript_{curr_session.id}.txt", "r"
        #         ) as txt_file:
        #             context["transcription"] = txt_file.read()
        # except:
        #     logger.warning("no session ID exising. setting a new one")

        return render(request, self.template_name, context=context)


class UserTranscriptionsView(TemplateView):
    """List of all current recordings that the user has"""

    template_name = "main/user_transcriptions.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["media_url"] = f"{MEDIA_URL}recordings"
        context["transcs"] = Transcription.objects.all()
        return context


def upload_audio(request, session_id):
    if request.POST:
        try:
            session = get_object_or_404(RecodringSession, id=session_id)
            audio_blob = request.FILES["audio_blob"]
            device = request.POST["device"]
            recording = Recording(
                session=session_id,
                voice_recording=audio_blob,
                audio_type=device,
            )
            recording.save()

            session.recordings.append(str(recording.id))
            session.save()

            return JsonResponse({"success": True})
        except Exception as e:
            logger.error(f"<ALS>> Failed uploading audio: {e}")
            return JsonResponse({"success": False})
    else:
        return JsonResponse({"success": True})


def check_recordings(request, session_id: str, current_count: int):
    """Checks the number of recordings in the session and returns True if there are more recordings than the current_count
    Args:
        session_id (str): id of the session
        current_count (int): number of recordings in the session
    Returns:
        bool: True if there are more recordings than the current_count
    """
    session = get_object_or_404(RecodringSession, id=session_id)
    recordings = session.recordings
    if len(recordings) > current_count:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


def transcribe(request, session_id):
    if request.method == "POST":
        curr_session = RecodringSession.objects.get(id=session_id)
        session_path = f"{MEDIA_ROOT}/recordings/{session_id}"
        # Creating a new session
        RecodringSession.objects.create()

        files = sorted(glob.glob(f"{session_path}/*.wav"), key=os.path.getmtime)
        if len(files) > 0:
            transcription_file = f"{session_path}/transcript_{session_id}.txt"
            with open(transcription_file, "a") as txt_file:
                for idx, file in enumerate(files, start=1):
                    try:
                        txt = transcribe_api(file)
                    except Exception as e:
                        logger.error(f"<ALS>> Transcribe error: {e}")
                        return JsonResponse({"success": False, "content": f"{e}"})

                    txt_file.writelines(f"{idx}- {txt}\n")
            Transcription.objects.create(file=transcription_file, session=session_id)

            # closing current session
            curr_session.ended = make_aware(datetime.now())
            curr_session.save()

            return JsonResponse({"success": True, "content": txt})

        else:
            messages.warning(request, "No files to transcribe")
            return JsonResponse({"success": False, "content": "No files to transcribe"})

    else:
        return JsonResponse({"success": True})


def recordings(request, session_id):
    context = {}
    recordings_list = Recording.objects.filter(session=session_id)
    context["recordings"] = recordings_list
    return render(request, "main/partials/recordings.html", context=context)
