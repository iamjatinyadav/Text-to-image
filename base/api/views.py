from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..tasks import generate_image
from celery import group
from ..models import GeneratedImage

@csrf_exempt
def generate_images(request):
    # prompts = [
    #     "A red flying dog",
    #     "A piano ninja",
    #     "A footballer kid"
    # ]

    prompts = [
        'A flying car',
        'A Jumping Boy',
        'A bike in water'
    ]

    # Create a group of tasks to run in parallel
    job = group(generate_image.s(prompt) for prompt in prompts)
    result = job.apply_async()

    image_ids = result.get()

    # Get the URLs of the generated images
    image_urls = [request.build_absolute_uri(GeneratedImage.objects.get(id=image_id).image.url) for image_id in
                  image_ids]

    return JsonResponse({"message": "Image generation completed", "image_urls": image_urls})
