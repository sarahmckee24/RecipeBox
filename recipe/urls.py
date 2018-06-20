from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('recipeBox/', include('recipeBox.urls')),
    path('admin/', admin.site.urls),
]
