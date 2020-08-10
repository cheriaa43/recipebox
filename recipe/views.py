from django.shortcuts import render, HttpResponseRedirect, reverse
from recipe.models import Author, Recipe
from recipe.forms import AddRecipeForm, AddAuthorForm

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

def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                time_required=data.get('time_required'),
                instructions=data.get('instructions'),
                author=data.get('author')
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {"form": form})

def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data.get('name'),
                bio=data.get('bio')
        )
        return HttpResponseRedirect(reverse("homepage"))

    form = AddAuthorForm()
    return render(request, "generic_form.html", {"form": form})
