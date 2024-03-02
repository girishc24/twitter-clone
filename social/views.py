from django.shortcuts import render
from  . models import Profile
# Create your views here.

def home(request):
    return render(request, 'home.html',)

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    context = {"profiles": profiles}
    return render(request, 'profile_list.html', context)
