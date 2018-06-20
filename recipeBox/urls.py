from django.urls import path
from . import views 

app_name = 'recipeBox'

urlpatterns = [
    # /recipeBox/
    path('', views.index, name='index'),

    # /recipeBox/all_favorites/
    path('favorites/', views.all_favorites, name='all_favorites'),

    # /recipeBox/<recipe_id>/
    path('<recipe_id>/', views.detail, name='detail'),

    # /recipeBox/<recipe_id>/favorite/
    path('<recipe_id>/favorite/', views.favorite, name='favorite'),

    # /recipeBox/recipe/add/
    path('recipe/add/', views.create_recipe, name='create_recipe'),

    # /recipeBox/recipe/<recipe_id>/delete
    path('<recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),

    # /recipeBox/recipe/<recipe_id>/add/
    path('<recipe_id>/add/ingredients/', views.create_ingredients, name='create_ingredients'),

    # /recipeBox/recipe/<recipe_id/edit/ingredients
    path('<recipe_id>/edit/ingredients/<ingredients_id>', views.edit_ingredients, name='edit_ingredients'),

    # /recipeBox/recipe/
    path('<recipe_id>/add/steps/', views.create_steps, name='create_steps')
]