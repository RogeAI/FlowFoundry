from django.urls import path

from . import views


app_name = "web"

urlpatterns = [
    path("", views.about, name="about"),
    path("about/", views.about, name="about_alias"),
    path("workspace/", views.workspace, name="workspace"),
    path("session/", views.session, name="session"),
    path("api/workflows/prepare/", views.prepare_workflow, name="prepare_workflow"),
    path("api/sessions/respond/", views.respond_to_session, name="respond_to_session"),
]
