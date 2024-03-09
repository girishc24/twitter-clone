from django.shortcuts import render, redirect
from django.contrib import messages
from  . models import Profile, Meep
from . forms import MeepForm
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
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