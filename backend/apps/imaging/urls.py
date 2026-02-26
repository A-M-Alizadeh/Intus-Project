from django.urls import path

from . import views

urlpatterns = [
    path("process/", views.process_image, name="process-image"),
    path("analyze/", views.analyze_image, name="analyze-image"),
]
