from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.contrib.auth.models import Group

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            
            group = Group.objects.get(name='Users')
            user.groups.add(group)
            
            if user is not None:
                login(request, user)
                
            return redirect(reverse('meetups:main'))
        else:
            print("Authentication failed for the new user.")
        
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})
