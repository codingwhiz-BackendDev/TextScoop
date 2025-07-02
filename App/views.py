from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ImageText
import easyocr
from PIL import Image
import os

def index(request):
    print("=== DEBUG: View function called ===")
    print(f"Request method: {request.method}")
    
    if request.method == 'POST':
        print("=== DEBUG: POST request received ===")
        print(f"Files in request: {request.FILES}")
        
        # Handle multiple images directly from request.FILES
        images = request.FILES.getlist('image')
        print(f"=== DEBUG: Number of images: {len(images)} ===")
        extracted_texts = []
        
        if images:
            # Initialize EasyOCR reader (only once)
            try:
                reader = easyocr.Reader(['en'])
                print("=== DEBUG: EasyOCR initialized successfully ===")
            except Exception as e:
                print(f"=== DEBUG: Error initializing EasyOCR: {str(e)} ===")
                messages.error(request, f"Error initializing OCR: {str(e)}")
                return render(request, 'index.html', {
                    'extracted_texts': [],
                    'recent_images': ImageText.objects.all().order_by('-uploaded_at')[:10]
                })
            
            for i, image_file in enumerate(images):
                print(f"=== DEBUG: Processing image {i+1}: {image_file.name} ===")
                try:
                    # Create ImageText instance
                    image_text = ImageText(image=image_file)
                    image_text.save()
                    print(f"=== DEBUG: Image saved to database with ID: {image_text.id} ===")
                    
                    # Open the image using PIL
                    img = Image.open(image_text.image.path)
                    print(f"=== DEBUG: Image opened successfully: {img.size} ===")
                    
                    # Extract text using EasyOCR
                    print("=== DEBUG: Starting OCR text extraction ===")
                    results = reader.readtext(image_text.image.path)
                    print(f"=== DEBUG: OCR completed. Found {len(results)} text regions ===")
                    
                    # Extract text from results
                    text_parts = []
                    for (bbox, text, prob) in results:
                        if prob > 0.5:  # Only include text with confidence > 50%
                            text_parts.append(text)
                    
                    extracted_text = ' '.join(text_parts)
                    print(f"=== DEBUG: Extracted text: {extracted_text[:100]} ===")
                    
                    # Update the model with extracted text
                    image_text.extracted_text = extracted_text.strip()
                    image_text.save()
                    print(f"=== DEBUG: Text saved to database ===")
                    
                    extracted_texts.append({
                        'filename': image_text.filename(),
                        'text': extracted_text.strip(),
                        'id': image_text.id
                    })
                    
                except Exception as e:
                    print(f"=== DEBUG: Error processing {image_file.name}: {str(e)} ===")
                    print(f"=== DEBUG: Error type: {type(e)} ===")
                    import traceback
                    print(f"=== DEBUG: Full traceback: {traceback.format_exc()} ===")
                    messages.error(request, f"Error processing {image_file.name}: {str(e)}")
            
            if extracted_texts:
                print(f"=== DEBUG: Successfully processed {len(extracted_texts)} images ===")
                messages.success(request, f"Successfully processed {len(extracted_texts)} image(s)")
            else:
                print("=== DEBUG: No images were successfully processed ===")
                messages.warning(request, "No images were processed successfully")
        else:
            print("=== DEBUG: No images found in request ===")
            messages.error(request, "No images were uploaded")
    
    return render(request, 'index.html', {
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
    
    return redirect('index')
