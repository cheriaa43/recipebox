
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import HttpResponseRedirect, render, reverse

from recipe.forms import AddAuthorForm, AddRecipeForm, LoginForm, EditRecipe
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


@login_required
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
                author=request.user.author
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def add_author(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = AddAuthorForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
                Author.objects.create(
                    name=data.get('name'),
                    user=new_user,
                    bio=data.get('bio')
                )
            return HttpResponseRedirect(reverse("homepage"))
    else:
        return HttpResponseForbidden("Unauthorized Access Forbidden")

    form = AddAuthorForm()
    return render(request, "generic_form.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get("username"), password=data.get("password"))
            if user:
                login(request, user) # sets session cookie
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))

    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))

def edit_recipe(request, id):
    html = 'generic_form.html'
    instance = Recipe.objects.get(id=id)
    if request.method == 'POST':
        form = EditRecipe(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("homepage"))

    form = EditRecipe(instance=instance)

    return render(request, html, {'form': form})


def add_fave(request, id):
    recipe = None
    user = None
    try:
        recipe = Recipe.objects.get(id=id)
        user = Author.objects.get(name=request.user.username)
        user.faves.add(recipe)
        user.save()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(reverse("homepage"))
