from django.contrib import admin
from .models import ImageText

# Register your models here.
@admin.register(ImageText)
class ImageTextAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['extracted_text']
    readonly_fields = ['uploaded_at']
