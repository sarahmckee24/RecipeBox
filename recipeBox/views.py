from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Recipe, Ingredients, Steps
from .forms import RecipeForm, IngredientsForm, StepsForm


""" class IndexView(generic.ListView):
    template_name = 'recipeBox/index.html'
    context_object_name = 'all_recipes'

    def get_queryset(self):
        return Recipe.objects.all()

class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipeBox/detail.html'

class RecipeCreate(CreateView):
    model = Recipe
    fields = ['name', 'author', 'prep_time', 'cook_time']

class RecipeUpdate(UpdateView):
    model = Recipe
    fields = ['name', 'author', 'prep_time', 'cook_time']

class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipeBox:index')

class IngredientsCreate(CreateView):
    model = Ingredients
    fields = ['name', 'amount', 'measurement'] """

def create_recipe(request):
    form = RecipeForm(request.POST or None)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.save()
        return render(request, 'recipeBox/detail.html', {'recipe': recipe})
    context = {
        "form": form,
    }
    return render(request, 'recipeBox/create_recipe.html', context)

def create_ingredients(request, recipe_id):
    form = IngredientsForm(request.POST or None)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if form.is_valid():
        ingredient_list = recipe.ingredients_set.all()
        for i in ingredient_list:
            if i.name == form.cleaned_data.get("name"):
                context = {
                    'recipe': recipe,
                    'form': form,
                    'error_message': 'You already added that ingredient',
                }
                return render(request, 'recipeBox/create_ingredients.html', context)
        ingredient = form.save(commit=False)
        ingredient.recipe_id = recipe
        ingredient.save()
        return render(request, 'recipeBox/detail.html', {'recipe': recipe})
    context = {
        'recipe': recipe,
        'form': form,
    }
    return render(request, 'recipeBox/create_ingredients.html', context)

def edit_ingredients(request, recipe_id, ingredients_id):
    ingredient = get_object_or_404(Ingredients, recipe_id=recipe_id, pk=ingredients_id)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    form = IngredientsForm(request.POST, instance = ingredient)
    if form.is_valid():
        i = form.save(commit=False)
        i.recipe_id = recipe
        i.save()
        return render(request, 'recipeBox/detail.html', {'recipe': recipe, 'ingredient': ingredient})

    context = {
        'recipe': recipe,
        'ingredient': ingredient,
        'form': form,
    }
    print (ingredient)
    return render(request, 'recipeBox/edit_ingredients.html', context)

def create_steps(request, recipe_id):
    form = StepsForm(request.POST or None)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if form.is_valid():
        steps_list = recipe.steps_set.all()
        for s in steps_list:
            if s.step_number == form.cleaned_data.get("step_number"):
                context = {
                    'recipe': recipe,
                    'form': form,
                    'error_message': 'You already added that step',
                }
                return render(request, 'recipeBox/create_steps.html', context)
        step = form.save(commit=False)
        step.recipe_id = recipe
        step.save()
        return render(request, 'recipeBox/detail.html', {'recipe': recipe})
    context = {
        'recipe': recipe,
        'form': form,
    }
    return render(request, 'recipeBox/create_steps.html', context)

def delete_recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.delete()
    recipes = Recipe.objects.all()
    return render(request, 'recipeBox/index.html', {'recipes': recipes})

def delete_ingredients(request, recipe_id, ingredients_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredient = Ingredients.objects.get(pk=ingredients_id)
    ingredient.delete()
    return render(request, 'recipeBox/detail.html', {'recipe': recipe})

def delete_steps(request, recipe_id, steps_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    step = Steps.objects.get(pk=steps_id)
    step.delete()
    return render(request, 'recipeBox/detail.html', {'recipe': recipe})

def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipes = Recipe.objects.all()
    ingredients_results = Ingredients.objects.all()
    query = request.GET.get("q")
    if query:
        recipes = recipes.filter(
            Q(name__icontains=query) |
            Q(cook_time__icontains=query) |
            Q(prep_time__icontains=query)
        ).distinct()
        ingredients_results = ingredients_results.filter(
            Q(name__icontains=query)
        ).distinct()
        return render(request, 'recipeBox/index.html', {
            'recipes': recipes,
            'ingredients': ingredients_results,
        })
    else:
        return render(request, 'recipeBox/detail.html', {'recipe': recipe})

def index(request):
    recipes = Recipe.objects.all()
    ingredients_results = Ingredients.objects.all()
    query = request.GET.get("q")
    if query:
        recipes = recipes.filter(
            Q(name__icontains=query) |
            Q(cook_time__icontains=query) |
            Q(prep_time__icontains=query)
        ).distinct()
        ingredients_results = ingredients_results.filter(
            Q(name__icontains=query)
        ).distinct()
        return render(request, 'recipeBox/index.html', {
            'recipes': recipes,
            'ingredients': ingredients_results,
        })
    else:
        return render(request, 'recipeBox/index.html', {'recipes': recipes})

def all_favorites(request):
    favorites = Recipe.objects.filter(is_favorite = True)
    recipes = Recipe.objects.all()
    ingredients_results = Ingredients.objects.all()
    query = request.GET.get("q")
    if query:
        recipes = recipes.filter(
            Q(name__icontains=query) |
            Q(cook_time__icontains=query) |
            Q(prep_time__icontains=query)
        ).distinct()
        ingredients_results = ingredients_results.filter(
            Q(name__icontains=query)
        ).distinct()
        return render(request, 'recipeBox/index.html', {
            'recipes': recipes,
            'ingredients': ingredients_results,
        })
    else:
        return render(request, 'recipeBox/favorite.html', {'recipes': favorites})

def favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    try:
        if recipe.is_favorite:
            recipe.is_favorite = False
        else:
            recipe.is_favorite = True
        recipe.save()
    except (KeyError, Recipe.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

