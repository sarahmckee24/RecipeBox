from django.contrib import admin
from .models import Recipe, Ingredients, Steps

admin.site.register(Recipe)
admin.site.register(Ingredients)
admin.site.register(Steps)
