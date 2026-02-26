import base64
from io import BytesIO

import cv2
import numpy as np
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


@csrf_exempt
@require_POST
def analyze_image(request):
    """Detect a likely liver region and return a bounding box with confidence."""
    image_file = request.FILES.get("image")
    if not image_file:
        return JsonResponse({"error": "Missing image"}, status=400)

    try:
        pil_img = Image.open(image_file).convert("RGB")
    except Exception:
        return JsonResponse({"error": "Invalid image file"}, status=400)

    np_img = np.array(pil_img)
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)

    # Simple heuristic: threshold bright tissue-like regions and take the largest contour as ROI.
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return JsonResponse(
            {
                "detected": False,
                "confidence": 0.0,
                "bounding_box": {"x": 0, "y": 0, "width": 0, "height": 0},
            }
        )

    largest = max(contours, key=cv2.contourArea)
    x, y, width, height = cv2.boundingRect(largest)
    area = float(cv2.contourArea(largest))
    img_area = float(np_img.shape[0] * np_img.shape[1])
    confidence = max(0.0, min(1.0, area / img_area))

    return JsonResponse(
        {
            "detected": True,
            "confidence": round(confidence, 2),
            "bounding_box": {
                "x": int(x),
                "y": int(y),
                "width": int(width),
                "height": int(height),
            },
        }
    )
