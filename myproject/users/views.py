from email import message
from django.shortcuts import render, redirect
from users.models import Profile
from projects.models import Project
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.



def loginUser(request):

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check user
        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, 'Username does not exist!')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'User successfully logged in!')
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'User successfully logged out!')
    return redirect('login')

def profile(request):

    profiles = Profile.objects.all()


    context = {
        'profiles': profiles
    }

    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact='')
    otherSkills = profile.skill_set.filter(description='')

    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills,
    }

    return render(request, 'users/user-profile.html', context)
