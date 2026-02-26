from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from apps.imaging.views import analyze_image


def health(request):
    return HttpResponse("OK")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/imaging/", include("apps.imaging.urls")),
    path("analyze/", analyze_image),
    path("", health),
]
