from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from backend.views import api_root

def home(request):
    return HttpResponse("API is running")

urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('', include('backend.urls')),
]



