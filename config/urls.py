from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.authtoken.views import obtain_auth_token


def home(request):
    return HttpResponse("API is running")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("backend.urls")),
    path("api/login/", obtain_auth_token),

]



