from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Recipe


@login_required(login_url='login')
def index(request):
    errors = {}
    if request.method == 'POST':
        recipe_name = request.POST.get('recipe_name', '')
        ingredient = request.POST.get('ingredient', '')
        description = request.POST.get('recipe_description', '')
        recipe_image = request.FILES.get('recipe_image')
        print(recipe_name)
        if recipe_name == "":
            errors['recipe_name'] = "You have to enter a recipe name"
        if ingredient == "":
            errors['ingredient'] = "You have to enter an ingredient"
        if description == "":
            errors['description'] = "You have to enter a description"

        # If no errors, save to database
        if not errors:
            Recipe.objects.create(
                recipe_name=recipe_name,
                ingredient=ingredient,
                description=description,
                recipe_image=recipe_image
            )
            messages.success(request, 'Recipe added successfully!')
            return redirect('index')
    queryset=Recipe.objects.all()
    context = {'errors': errors,'queryset':queryset}
    return render(request, "index.html", context)


@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')

@login_required(login_url='login')
def delete_recipe(request,id):
    queryset=Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('index')

@login_required(login_url='login')
def update(request,id):
    recipe=Recipe.objects.get(id=id)
    if request.method == 'POST':
        recipe_name = request.POST.get('recipe_name', '')
        ingredient = request.POST.get('ingredient', '')
        description = request.POST.get('recipe_description', '')
        recipe_image = request.FILES.get('recipe_image')

        # Update the recipe fields
        recipe.recipe_name = recipe_name
        recipe.ingredient = ingredient
        recipe.description = description

        # Only update image if a new one is uploaded
        if recipe_image:
            recipe.recipe_image = recipe_image

        recipe.save()
        messages.success(request, 'Recipe updated successfully!')
        return redirect('index')

    context={'recipe':recipe}
    return render(request,"update.html",context)
def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('registration')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('registration')

        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')

    return render(request, 'registration.html')



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')

