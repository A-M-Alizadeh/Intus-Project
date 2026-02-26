from django.http import HttpResponse


def home(request):
    """Simple root view so / returns a response."""
    return HttpResponse(
        "<p>Intus Django project is running.</p>"
        "<p>Try <a href='/admin/'>/admin/</a> or <a href='/api/example/'>/api/example/</a></p>",
        content_type="text/html",
    )
