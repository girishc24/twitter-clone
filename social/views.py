from django.shortcuts import render, redirect
from django.contrib import messages
from  . models import Profile
# Create your views here.

def home(request):
    return render(request, 'home.html',)

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
        if request.method == 'POST':
            current_user_profile =request.user.profile
            action=request.POST['follow']

            if action == "UnFollow":
                current_user_profile.follows.remove(profile)
            elif action == "Follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        context = {"profilenew": profile}
        return render(request, 'profile.html', context)
    else:
        messages.success(request,("You must be Login for viewing this page"))
        return redirect('home')