from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .ocr_utils import ocr_image
from PIL import Image
import io
import errno
import logging


logger = logging.getLogger(__name__)

# Create your views here.
def ocr_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        action = request.POST.get('action')

        try:
            if action == 'ocr':
                text = ocr_image(image)

                # Create the HttpResponse object with the appropriate PDF headers
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="ocr_result.pdf"'
                
                # Create the PDF object, using the response object as its "file."
                p = canvas.Canvas(response, pagesize=letter)
                
                # Set up the page
                width, height = letter
                p.setFont("Helvetica", 12)
                y = height - 40  # Start a bit down the page
                
                # Split the text into lines and write them to the PDF
                for line in text.split('\n'):
                    p.drawString(40, y, line)
                    y -= 15  # Move down the page
                
                # Finalize the PDF
                p.showPage()
                p.save()
                
                return response

            elif action == 'convert_to_pdf':
                # Open the image using Pillow
                img = Image.open(image)

                # Create a BytesIO buffer to hold the PDF data
                pdf_buffer = io.BytesIO()

                # Save the image as a PDF
                img.save(pdf_buffer, format='PDF')

                # Get the value of the BytesIO buffer and write it to the response
                pdf_buffer.seek(0)
                response = HttpResponse(pdf_buffer, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="converted_image.pdf"'

                return response

        except IOError as e:
            if e.errno == errno.EPIPE:
                logger.error("Broken pipe: client disconnected before the response could be completed.")
            else:
                logger.error(f"IOError: {e}")
            return HttpResponse("An error occurred while processing your request.", status=500)
        
        except Exception as e:
            logger.error(f"Error: {e}")
            return HttpResponse("An unexpected error occurred.", status=500)

    return render(request, 'upload.html')


