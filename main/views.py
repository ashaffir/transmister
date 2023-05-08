import os
import glob
from datetime import datetime
from typing import Any, Dict

from django.views.generic import TemplateView
from django.utils.timezone import make_aware
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from transmister.settings import MEDIA_ROOT, MEDIA_URL
from .models import RecodringSession, Recording, Transcription, Control
from .utils import (
    transcribe_api,
    calculate_audio_duration,
    get_recording_duration,
    logger,
)


class HomeView(LoginRequiredMixin, TemplateView):
    """Home page"""

    template_name = "main/recording.html"

    def get(self, request):
        context = {}
        # Getting the last open session
        curr_session = RecodringSession.objects.filter(
            user=request.user, ended__isnull=True
        ).last()
        if not curr_session:
            curr_session = RecodringSession.objects.create(user=request.user)

        context["session"] = curr_session
        context["recordings"] = Recording.objects.filter(session=curr_session.id)

        return render(request, self.template_name, context=context)


class UserTranscriptionsView(LoginRequiredMixin, TemplateView):
    """List of all current recordings that the user has"""

    template_name = "main/user_transcriptions.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["media_url"] = f"{MEDIA_URL}recordings"
        context["transcs"] = Transcription.objects.filter(user=self.request.user)
        return context


@login_required
def upload_audio(request, session_id):
    if request.POST:
        try:
            session = get_object_or_404(RecodringSession, id=session_id)
            audio_blob = request.FILES["audio_blob"]
            device = request.POST["device"]
            recording = Recording(
                user=request.user,
                session=session_id,
                voice_recording=audio_blob,
                duration=calculate_audio_duration(audio_blob),
                audio_type=device,
            )
            recording.save()

            session.recordings.append(str(recording.id))
            session.save()

            logger.info(f"<ALS>> recording {recording.id} saved")
            return JsonResponse({"success": True})
        except Exception as e:
            logger.error(f"<ALS>> Failed uploading audio: {e}")
            return JsonResponse({"success": False})
    else:
        return JsonResponse({"success": True})


@login_required
def check_recordings(request, session_id: str, current_count: int):
    """Checks the number of recordings in the session and returns True if there are more
        recordings than the current_count
    Args:
        session_id (str): id of the session
        current_count (int): number of recordings in the session
    Returns:
        bool: True if there are more recordings than the current_count
    """
    recordings = Recording.objects.filter(session=session_id).count()
    if recordings > current_count:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@login_required
def recordings(request, session_id):
    context = {}
    context["recordings"] = Recording.objects.filter(session=session_id)
    return render(request, "main/partials/recordings.html", context=context)


@login_required
def clear_session(request, session_id):
    session = get_object_or_404(RecodringSession, id=session_id)
    recordings_list = Recording.objects.filter(session=session_id)
    for recording in recordings_list:
        recording.delete()

    session.recordings.clear()
    session.ended = make_aware(datetime.now())
    session.save()

    return JsonResponse({"success": True})


@login_required
def delete_recording(request):
    recording = get_object_or_404(Recording, id=request.GET.get("recording_id"))
    session = get_object_or_404(RecodringSession, id=recording.session)
    session.recordings.remove(str(recording.id))
    session.save()

    recording.delete()
    return JsonResponse({"success": True})


@login_required
def transcribe(request, session_id):
    user = request.user
    if request.method == "POST":
        curr_session = RecodringSession.objects.get(id=session_id)
        session_path = f"{MEDIA_ROOT}/recordings/user_{user.id}/{session_id}"
        # Creating a new session
        RecodringSession.objects.create(user=user)

        files = sorted(glob.glob(f"{session_path}/*.wav"), key=os.path.getmtime)
        total_audio_length = 0
        if len(files) > 0:
            transcription_file = f"{session_path}/transcript_{session_id}.txt"
            language = request.POST["language"]
            with open(transcription_file, "a") as txt_file:
                for idx, file in enumerate(files, start=1):
                    try:
                        total_audio_length += get_recording_duration(file)

                        if user.get_available_minutes() < total_audio_length:
                            return JsonResponse(
                                {"success": False, "content": f"balance"}
                            )

                        else:
                            txt = transcribe_api(file, language)
                    except Exception as e:
                        logger.error(f"<ALS>> Transcribe error: {e}")
                        return JsonResponse({"success": False, "content": f"{e}"})

                    txt_file.writelines(f"{idx}- {txt}\n")

                # Adding blank rows
                blank_rows, created = Control.objects.get_or_create(name="blank_rows")
                if created:
                    blank_rows.int_value = 3
                    blank_rows.save()

                for i in range(blank_rows.int_value):
                    txt_file.writelines("\n")

            transcription = Transcription.objects.create(
                file=transcription_file,
                user=user,
                session=session_id,
                duration=total_audio_length,
                language=language,
            )

            # Cost Calculation
            transcription_cost = total_audio_length * settings.PRICE_PER_MINUTE
            transcription.cost = round(transcription_cost, 3)
            transcription.save()

            # Deduct transcription cost from user account
            user.balance -= transcription_cost
            user.save()

            # closing current session
            curr_session.ended = make_aware(datetime.now())
            curr_session.save()

            with open(transcription_file, "r") as f:
                txt_content = f.read()
            return JsonResponse({"success": True, "content": txt_content})

        else:
            messages.warning(request, "No files to transcribe")
            return JsonResponse({"success": False, "content": "No files to transcribe"})

    else:
        return JsonResponse({"success": True})
