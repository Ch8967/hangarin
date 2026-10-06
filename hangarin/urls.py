from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from tasks import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("login/", RedirectView.as_view(pattern_name="account_login", query_string=True), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("tasks/new/", views.task_create, name="task_create"),
    path("", views.home, name="home"),

    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),
]
