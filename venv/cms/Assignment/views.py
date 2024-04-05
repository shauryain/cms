from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Assignment.forms import UserRegistrationForm, ContentForm, SearchForm
from Assignment.models import User, Content


# Create your views here.

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/registration_form.html', {'form': form})

@login_required
def create_content(request):
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            content = form.save(commit=False)
            content.user = request.user
            content.save()
            messages.success(request, 'Content created successfully.')
            return redirect('home')
    else:
        form = ContentForm()
    return render(request, 'content/content_form.html', {'form': form})

def search_content(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            contents = Content.objects.filter(
                models.Q(title__icontains=search_term) |
                models.Q(body__icontains=search_term) |
                models.Q(summary__icontains=search_term) |
                models.Q(categories__icontains=search_term)
            )
            return render(request, 'content/content_list.html', {'contents': contents})
    else:
        form = SearchForm()
    return render(request, 'content/search_form.html', {'form': form})

@login_required
def view_content(request, content_id):
    content = Content.objects.get(id=content_id)
    if request.user == content.user or request.user.is_staff:
        return render(request, 'content/view_content.html', {'content': content})
    else:
        messages.error(request, 'You do not have permission to view this content.')
        return redirect('home')

@login_required
def edit_content(request, content_id):
    content = Content.objects.get(id=content_id)
    if request.user == content.user or request.user.is_staff:
        if request.method == 'POST':
            form = ContentForm(request.POST, instance=content)
            if form.is_valid():
                form.save()
                messages.success(request, 'Content updated successfully.')
                return redirect('home')
        else:
            form = ContentForm(instance=content)
        return render(request, 'content/content_form.html', {'form': form})
    else:
        messages.error(request, 'You do not have permission to edit this content.')
        return redirect('home')

@login_required
def delete_content(request, content_id):
    content = Content.objects.get(id=content_id)
    if request.user == content.user or request.user.is_staff:
        if request.method == 'POST':
            content.delete()
            messages.success(request, 'Content deleted successfully.')
            return redirect('home')
        return render(request, 'content/confirm_delete.html', {'content': content})
    else:
        messages.error(request, 'You do not have permission to delete this content.')
        return redirect('home')

