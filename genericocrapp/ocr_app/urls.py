from django.urls import path
from .views import ocr_view

# create urlpatterns here

urlpatterns = [
    path('', ocr_view, name='ocr_view')

]
