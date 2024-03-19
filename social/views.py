from django.shortcuts import render, redirect
from django.contrib import messages
from  . models import Profile, Meep
from . forms import MeepForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Create your views here.



def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None )
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request,("Your Meep is Saved"))
                return redirect('home')

        meeps=Meep.objects.all().order_by("-created_at")
        context={"meeps": meeps, "form":form}
        return render(request, 'home.html', context)
    else:
        meeps=Meep.objects.all().order_by("-created_at")
        context={"meeps": meeps}
        return render(request, 'home.html', context)

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        context = {"profiles": profiles}
        return render(request, 'profile_list.html', context)
    else:
        messages.success(request,("You must be Login for viewing this page"))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
        meeps=Meep.objects.filter(user_id=pk)

        if request.method == 'POST':
            current_user_profile =request.user.profile
            action=request.POST['follow']

            if action == "UnFollow":
                current_user_profile.follows.remove(profile)
            elif action == "Follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        context = {"profilenew": profile, "meeps":meeps}
        return render(request, 'profile.html', context)
    else:
        messages.success(request,("You must be Login for viewing this page"))
        return redirect('home')
    
def login(request):
    if request.method == "POST":
        username= request.POST['username']
        password= request.POST['pass']
        user =authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request,("Login Successfully"))
            return redirect('home')
        else:
            messages.success(request,("Can't Able to Login"))
            return redirect('login')
    else:    
        return render(request, "login.html")

def logout(request):
    auth_logout(request)
    messages.success(request,("You Have Been Logout"))
    return redirect('home')