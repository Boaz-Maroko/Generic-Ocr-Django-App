from django.shortcuts import render
from django.http import HttpResponse
from .ocr_utils import ocr_image

# Create your views here.
def ocr_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        text = ocr_image(image)
        # Replace newline characters with <br> tags
        text_with_br = text.replace('\n', '<br>')
        return render(request, 'result.html', {'text': text_with_br})
    return render(request, 'upload.html')


