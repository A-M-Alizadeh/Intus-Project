from django.db import models

from core.models import TimeStampedModel


class ExampleItem(TimeStampedModel):
    """Example model showing how to inherit from TimeStampedModel."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
