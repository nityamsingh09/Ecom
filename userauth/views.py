from django.shortcuts import render,redirect
from userauth.forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login, authenticate,get_user_model,logout
from django.contrib import messages
from django.conf import settings

from userauth.models import Profile

# User = settings.AUTH_USER_MODEL
User = get_user_model()

# Create your views here.
def register_view(request):
    if request.method=="POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user=form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hey {username}, your account was created successfully!')
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('web:index')
    else:
         form = UserRegisterForm()
    
    context= {
        'form': form,
            }
    return render(request, 'userauth/sign-up.html', context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already logged in as {request.user.username}.")
        return redirect('web:index')
    
    if request.method == "POST":
        email =request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user=User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('web:index')
            else:
                messages.warning(request,"User Does not exist , create an account.")
                
        except:
            messages.warning(request, f"User with email {email} does not exist.")

       
    context={

    }
    return render(request,"userauth/sign-in.html",context)


def logout_view(request):
    logout(request)
    messages.warning(request, "You have been logged out successfully.")
    return redirect('userauth:sign-in')

def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":  
        form = ProfileForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
           new_form = form.save(commit=False)
           new_form.user = request.user
           new_form.save()
           
           messages.success(request, "Your profile has been updated successfully.")
           return redirect('web:dashboard')
    else:
        form = ProfileForm(instance=profile)
    context ={
        'form': form,
        'profile': profile,
    }
    return render(request, 'userauth/profile_update.html',context)
