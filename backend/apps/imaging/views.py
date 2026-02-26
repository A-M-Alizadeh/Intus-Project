import base64
from io import BytesIO

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from PIL import Image, ImageEnhance, ImageFilter


def _encode_image_to_base64(img: Image.Image) -> str:
    """Encode a Pillow image as base64 PNG so it can be returned in JSON."""
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


@csrf_exempt
@require_POST
def process_image(request):
    """
    Simulate arterial or venous phase from an uploaded image.

    - Arterial phase: boosts contrast.
    - Venous phase: applies soft gaussian smoothing.
    Returns both original and processed images as base64 strings.
    """
    image_file = request.FILES.get("image")
    phase = request.POST.get("phase")

    if not image_file or phase not in {"arterial", "venous"}:
        return JsonResponse({"error": "Missing or invalid image/phase"}, status=400)

    try:
        img = Image.open(image_file).convert("RGB")
    except Exception:
        return JsonResponse({"error": "Invalid image file"}, status=400)

    # Arterial simulation: make contrast stronger.
    if phase == "arterial":
        enhancer = ImageEnhance.Contrast(img)
        processed = enhancer.enhance(1.8)
    else:  # venous
        # Venous simulation: apply gentle gaussian smoothing.
        processed = img.filter(ImageFilter.GaussianBlur(radius=2.5))

    original_b64 = _encode_image_to_base64(img)
    processed_b64 = _encode_image_to_base64(processed)

    return JsonResponse({"original": original_b64, "processed": processed_b64})
