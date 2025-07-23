from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ImageText
from PIL import Image
import pytesseract
import os
import logging 

# Get an instance of a logger for this module
logger = logging.getLogger(__name__)
 
TESSERACT_CMD_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
 
try:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_PATH
    logger.info(f"Tesseract command path set to: {pytesseract.pytesseract.tesseract_cmd}") 
    if not os.path.exists(TESSERACT_CMD_PATH):
        logger.critical(f"Tesseract executable NOT FOUND at configured path: {TESSERACT_CMD_PATH}. OCR will fail.")
        # Optionally, raise an exception or set a flag to disable OCR functionality
except Exception as e:
    
    logger.critical(f"FATAL ERROR: Could not set Tesseract command path to {TESSERACT_CMD_PATH}. Error: {e}", exc_info=True)
     
def index(request):
    return render(request, 'index.html')

def extract(request):
    extracted_texts = []  
    recent_images = ImageText.objects.all().order_by('-uploaded_at')[:10]

    if request.method == 'POST':
        images = request.FILES.getlist('image')

        if not images:  
            messages.error(request, "No images were uploaded.")
            # If no images, return here to prevent further processing
            return render(request, 'extract.html', {
                'extracted_texts': extracted_texts,
                'recent_images': recent_images
            })

        for i, image_file in enumerate(images):
            try:
                 
                image_text = ImageText(image=image_file)
                image_text.save() # This saves the file to MEDIA_ROOT

                 
                img_path = image_text.image.path
                logger.info(f"Attempting to process image: {img_path}")
                logger.info(f"Tesseract command path being used for extraction: {pytesseract.pytesseract.tesseract_cmd}")

                img = Image.open(img_path)

                 
                extracted_text = pytesseract.image_to_string(img)

                 
                image_text.extracted_text = extracted_text.strip()
                image_text.save()

                extracted_texts.append({
                    'filename': image_text.filename(), # Assuming filename() is a method on your model
                    'text': extracted_text.strip(),
                    'id': image_text.id
                })
                logger.info(f"Successfully extracted text from {image_file.name}")

            except pytesseract.TesseractNotFoundError:
                error_msg = (f"Error processing {image_file.name}: Tesseract executable not found. "
                             f"Attempted path: '{pytesseract.pytesseract.tesseract_cmd}'. "
                             "Please ensure Tesseract is installed correctly and the path in views.py is accurate.")
                messages.error(request, error_msg)
                logger.error(error_msg, exc_info=True) # Log full traceback for debugging
            except Exception as e:
                 
                error_msg = f"Unexpected error processing {image_file.name}: {str(e)}"
                messages.error(request, error_msg)
                logger.exception(error_msg) # This logs the error message AND the full Python traceback

        if extracted_texts:
            messages.success(request, f"Successfully processed {len(extracted_texts)} image(s)!")
        else:
            messages.warning(request, "No images were processed successfully.")
 
        recent_images = ImageText.objects.all().order_by('-uploaded_at')[:10]

    return render(request, 'extract.html', {
        'extracted_texts': extracted_texts,
        'recent_images': recent_images
    })


def delete_image(request, image_id):
    try:
        image_text = ImageText.objects.get(id=image_id)
         
        if image_text.image:
            if os.path.isfile(image_text.image.path):
                os.remove(image_text.image.path)
                logger.info(f"Deleted physical file: {image_text.image.path}")
        image_text.delete() # Delete the database record
        messages.success(request, "Image deleted successfully.")
    except ImageText.DoesNotExist:
        messages.error(request, "Image not found.")
        logger.warning(f"Attempted to delete non-existent image with ID: {image_id}")
    except Exception as e:
        messages.error(request, f"Error deleting image: {str(e)}")
        logger.exception(f"Error deleting image with ID: {image_id}") # Log full traceback

    return redirect('extract') # Redirect back to the extract page


def view_file(request, image_id):
    try:
        image_text = ImageText.objects.get(id=image_id) 
        return render(request, 'view_file.html', {'image_text': image_text})
    except ImageText.DoesNotExist:
        messages.error(request, "Image not found.")
        logger.warning(f"Attempted to view non-existent image with ID: {image_id}")
        return redirect('extract') 
    except Exception as e:
        messages.error(request, f"Error viewing file: {str(e)}")
        logger.exception(f"Error viewing file with ID: {image_id}") 
        return redirect('extract')