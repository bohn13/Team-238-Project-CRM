from io import BytesIO

from PIL import Image


def convert_to_webp(contents: bytes) -> bytes:
    image = Image.open(BytesIO(contents))
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")

    output = BytesIO()
    image.save(output, format="WEBP", quality=85)
    return output.getvalue()
