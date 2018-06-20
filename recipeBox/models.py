from django.db import models
from django.urls import reverse

class Recipe(models.Model):
    name = models.CharField(max_length=64)
    author = models.CharField(max_length=64)
    cook_time = models.CharField(max_length=64)
    prep_time = models.CharField(max_length=64)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipeBox:detail', kwargs={'pk':self.pk })

class Ingredients(models.Model):
    name = models.CharField(max_length=64)
    measurement = models.CharField(max_length=64)
    # deletes ingredients if recipe gets deleted
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    # returns name of ingredient instead of object
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipeBox:detail', kwargs={'pk':self.pk })

class Steps(models.Model):
    step_number = models.IntegerField()
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_info = models.CharField(max_length=2048)

    def __str__(self):
        return "Step " + str(self.step_number) + " for " + str(self.recipe_id) + ": " + str(self.step_info)

