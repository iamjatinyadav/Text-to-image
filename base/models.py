from django.db import models

# Create your models here.


class GeneratedImage(models.Model):
    prompt = models.CharField(max_length=255)
    image = models.ImageField(upload_to='generated_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for '{self.prompt}'"
