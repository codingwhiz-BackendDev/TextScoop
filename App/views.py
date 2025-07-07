from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ImageText
import easyocr
from PIL import Image
import os


def index(request):
    return render(request, 'index.html')

def extract(request): 
    if request.method == 'POST':          
        images = request.FILES.getlist('image')  
        extracted_texts = []
        
        if images: 
            try:
                reader = easyocr.Reader(['en'], gpu=True)
            except Exception as e: 
                messages.error(request, f"Error initializing OCR: {str(e)}")
                return render(request, 'extract.html', {
                    'extracted_texts': [],
                    'recent_images': ImageText.objects.all().order_by('-uploaded_at')[:10]
                })
            
            for i, image_file in enumerate(images): 
                try: 
                    image_text = ImageText(image=image_file)
                    image_text.save() 
                    
                    # Open the image using PIL
                    img = Image.open(image_text.image.path) 
                    
                    # Extract text using EasyOCR 
                    results = reader.readtext(image_text.image.path) 
                    
                    # Extract text from results
                    text_parts = []
                    for (bbox, text, prob) in results:
                        if prob > 0.2:  # Only include text with confidence > 50%
                            text_parts.append(text)
                    
                    extracted_text = '\n'.join(text_parts) 
                    
                    # Update the model with extracted text
                    image_text.extracted_text = extracted_text.strip()
                    image_text.save() 
                    
                    extracted_texts.append({
                        'filename': image_text.filename(),
                        'text': extracted_text.strip(),
                        'id': image_text.id
                    })
                    
                except Exception as e: 
                    messages.error(request, f"Error processing {image_file.name}: {str(e)}")
            
            if extracted_texts:
                 messages.success(request, f"Successfully processed {len(extracted_texts)} image(s)")
            else: 
                messages.warning(request, "No images were processed successfully")
        else: 
            messages.error(request, "No images were uploaded")
    
    return render(request, 'extract.html', {
        'extracted_texts': extracted_texts if 'extracted_texts' in locals() else [],
        'recent_images': ImageText.objects.all().order_by('-uploaded_at')[:10]
    })

def delete_image(request, image_id):
    try:
        image_text = ImageText.objects.get(id=image_id)
        image_text.delete()
        messages.success(request, "Image deleted successfully")
    except ImageText.DoesNotExist:
        messages.error(request, "Image not found")
    
    return redirect('extract')
