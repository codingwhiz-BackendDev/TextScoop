from django.db import models
import os

# Create your models here.

class ImageText(models.Model):
    image = models.ImageField(upload_to='uploads/')
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image {self.id} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    def filename(self):
        return os.path.basename(self.image.name)
