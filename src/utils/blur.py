from PIL import Image, ImageFilter
import requests
import io

def blur(url: str):
    img = Image.open(requests.get(url, stream=True).raw)
    img = img.filter(ImageFilter.GaussianBlur(radius = 15))
    img_byte = io.BytesIO()
    img.save(img_byte, format='PNG')
    return img_byte.getvalue()