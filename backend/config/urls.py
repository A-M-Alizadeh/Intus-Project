from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def health(request):
    return HttpResponse("OK")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/imaging/", include("apps.imaging.urls")),
    path("", health),
]
