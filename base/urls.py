from django.urls import path
from .views import generate_images, render_image_generation_page
# Api views

from .api import views as apiviews


urlpatterns = [
    path('', render_image_generation_page),
    path('generate/', generate_images),
]

urlpatternsApis = [
    path('api/v1/generate/', apiviews.generate_images, name='generate_images'),

]

urlpatterns += urlpatternsApis