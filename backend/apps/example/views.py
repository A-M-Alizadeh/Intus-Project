from django.http import JsonResponse
from django.views import View

from .models import ExampleItem


class ExampleItemListView(View):
    """List all example items as JSON."""

    def get(self, request):
        items = ExampleItem.objects.all().values("id", "name", "slug", "created_at")
        return JsonResponse({"items": list(items)})


class ExampleItemDetailView(View):
    """Return a single example item as JSON."""

    def get(self, request, pk):
        try:
            item = ExampleItem.objects.get(pk=pk)
        except ExampleItem.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse(
            {
                "id": item.id,
                "name": item.name,
                "slug": item.slug,
                "created_at": item.created_at.isoformat(),
                "updated_at": item.updated_at.isoformat(),
            }
        )
