from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "main"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "user-transcriptions/",
        views.UserTranscriptionsView.as_view(),
        name="user-transcriptions",
    ),
    path("upload/<str:session_id>/", views.upload_audio, name="upload"),
    path("transcribe/<str:session_id>/", views.transcribe, name="transcribe"),
    path("recordings/<str:session_id>/", views.recordings, name="recordings"),
    path(
        "check-recordings/<str:session_id>/<int:current_count>/",
        views.check_recordings,
        name="check-recordings",
    ),
    path("clear-session/<str:session_id>/", views.clear_session, name="clear-session"),
    path(
        "delete-recording/",
        views.delete_recording,
        name="delete-recording",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
