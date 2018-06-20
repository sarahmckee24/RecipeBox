from django import forms
from .models import Recipe, Ingredients, Steps

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'author', 'prep_time', 'cook_time']

class IngredientsForm(forms.ModelForm):
    recipe_id = forms.ModelChoiceField(queryset = Recipe.objects.all())
    class Meta:
        model = Ingredients
        fields = ['name', 'measurement', 'recipe_id']

class StepsForm(forms.ModelForm):
    recipe_id = forms.ModelChoiceField(queryset = Recipe.objects.all())
    class Meta:
        model = Steps
        fields = ['step_number', 'step_info']

