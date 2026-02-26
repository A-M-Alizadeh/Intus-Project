from django.urls import path

from . import views

urlpatterns = [
    path("", views.ExampleItemListView.as_view(), name="example-item-list"),
    path("<int:pk>/", views.ExampleItemDetailView.as_view(), name="example-item-detail"),
]
