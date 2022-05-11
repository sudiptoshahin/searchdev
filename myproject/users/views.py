from django.shortcuts import render, redirect
from users.models import Profile
from projects.models import Project
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm

from .utils import searchProfiles, paginateProfiles

# Create your views here.

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account is created successfully')
            login(request, user)
            return redirect('edit_account')
        else:
            messages.error(request, 'An error has occured during registration!')

    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login_register.html', context)

def loginUser(request):
    page = 'login'
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
            messages.info(request, 'User successfully logged in!')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or password incorrect')

    context = {
        'page': page
    }

    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request, 'User successfully logged out!')
    return redirect('login')


def profile(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 2)

    context = {
        'profiles': profiles,
        'custom_range': custom_range,
        'search_query': search_query
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


@login_required(login_url='login')
def userAccount(request):

    profile = request.user.profile

    skills = profile.skill_set.exclude(description__exact='')
    otherSkills = profile.skill_set.filter(description='')
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'skills': skills,
        'otherSkills': otherSkills,
        'projects': projects,
    }

    return render(request, 'users/useraccount.html', context)

# update
@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {
       'form': form,
    }

    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill added successfully1!')
            return redirect('account')

    context = {
        'form': form,
    }

    return render(request, 'users/skill-form.html', context)


# update user skill
@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile

    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully!')
            return redirect('account')

    context = {
        'form': form,
    }

    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile 

    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        return redirect('account')

    context = {
        'object': skill,
    }

    return render(request, 'delete_template.html', context)