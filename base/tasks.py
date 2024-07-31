import requests
from celery import shared_task
from django.conf import settings
from .models import GeneratedImage
from django.core.files.base import ContentFile
import base64


@shared_task
def generate_image(prompt):
    headers = {
        "Authorization": f"Bearer {settings.STABILITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
    }

    response = requests.post(settings.STABILITY_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        image_data = response.json()
        image_base64 = image_data['artifacts'][0]['base64']
        image_content = base64.b64decode(image_base64)

        generated_image = GeneratedImage(prompt=prompt)
        generated_image.image.save(f"{prompt}.png", ContentFile(image_content), save=True)

        return generated_image.id
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")