
from django.shortcuts import render,redirect
from .forms import CustomRegisterForm
#from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from django.contrib import messages
def register(request):
    #available post request in this instance
    if request.method=="POST":
        register_form = CustomRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request,"New account created, login to get started")
            return redirect('register')

    else:
        register_form = CustomRegisterForm()
    return render(request, 'register.html', {'register_form': register_form})

    # to design register page install crispy as pip install django-crispy-forms and add to settings 