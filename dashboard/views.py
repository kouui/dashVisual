from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users
# Create your views here.


#@login_required(login_url='login')
#@allowed_users(allowed_roles=["admin", "guest"])
def home(request):
    return render(request, "dashboard/dashboard.html")


@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='guest')
            user.groups.add(group)

            #Customer.objects.create(user=user)

            messages.success(request, f'Account was created for {username}')
            return redirect('login')
        else:
            messages.info(request, "Registration failed.")

    context = {'form':form}
    return render(request, 'dashboard/register.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, f'Username or Password is incorrect')
            #return redirect("login")
    context = {}
    return render(request, 'dashboard/login.html', context)

def logoutUser(request):
    logout(request)

    return redirect('login')
