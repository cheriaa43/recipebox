from django.shortcuts import render
from recipe.models import Author, Recipe

# Create your views here.
def index(request):
    my_recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipe_box": "Cheria's Recipe Box", "recipes": my_recipes})


def author_info(request, author_id):
    this_author = Author.objects.filter(id=author_id).first()
    recipe_contributed = Recipe.objects.filter(author=this_author)
    return render(request, "author_info.html", {"author": this_author, "recipes": recipe_contributed})


def recipe_info(request, recipe_id):
    this_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_info.html", {"recipe": this_recipe})

