from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views

urlpatterns = [
    path('', include("products.urls")),
    path('admin/', admin.site.urls),    
]
