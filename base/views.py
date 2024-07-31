from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import generate_image
from celery import group
from .models import GeneratedImage
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Create your views here.


def render_image_generation_page(request):
    return render(request, 'base/index.html')

@csrf_exempt
def generate_images(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        data = json.loads(request.body)
        prompts = data.get('prompts', [])
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON in request body"}, status=400)

    if not prompts:
        return JsonResponse({"error": "No prompts provided"}, status=400)


    print(prompts)

    # Create a group of tasks to run in parallel
    job = group(generate_image.s(prompt) for prompt in prompts)
    result = job.apply_async()

    # Get the channel layer
    channel_layer = get_channel_layer()

    # Wait for all tasks to complete
    image_ids = result.get()

    # Process results
    image_urls = []
    for image_id in image_ids:
        try:
            generated_image = GeneratedImage.objects.get(id=image_id)
            image_url = request.build_absolute_uri(generated_image.image.url)
            image_urls.append(image_url)

            # Send real-time update
            async_to_sync(channel_layer.group_send)(
                "image_generation",
                {
                    "type": "image.update",
                    "message": {
                        "prompt": generated_image.prompt,
                        "url": image_url
                    }
                }
            )
        except GeneratedImage.DoesNotExist:
            pass
        except Exception as e:
            print(f"Error processing image {image_id}: {str(e)}")

    return JsonResponse({"message": "Image generation completed", "image_urls": image_urls})
