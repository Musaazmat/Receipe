from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
import time

# authentication check weather password is same as username & login is session which keep session maintain & logout method for logout from session method and application
from django.contrib.auth import authenticate, login, logout

#login required
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login/')
def receipes(request):
    
    if request.method == "POST":
        
        data = request.POST

        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        Receipe.objects.create(
            receipe_name = receipe_name,
            receipe_description = receipe_description,
            receipe_image = receipe_image,
        )
    
        return redirect('receipes')

    queryset = Receipe.objects.all()
    
    if request.GET.get('search'):
        queryset = queryset.filter(Q(receipe_name__icontains = request.GET.get('search')) | Q(receipe_description__icontains = request.GET.get('search')))
        
    total_receipes = queryset.count()
    context = {'receipes': queryset, 'total_receipes': total_receipes}
    return render (request, 'receipes.html', context)


@login_required(login_url='/login/')
def delete_receipe(request, id):
    print(id)
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect("receipes")


def delete_all(request):
    queryset = Receipe.objects.all()
    queryset.delete()
    return redirect("receipes")


@login_required(login_url='/login/')
def update_receipe(request, id):
        queryset = Receipe.objects.get(id = id)
        
        if request.method == "POST":
            
            data = request.POST

            receipe_name = data.get('receipe_name')
            receipe_description = data.get('receipe_description')
            receipe_image = request.FILES.get('receipe_image')
            
            queryset.receipe_name = receipe_name
            queryset.receipe_description = receipe_description
            
            if receipe_image:
                queryset.receipe_image = receipe_image
                
                queryset.save()
                return redirect('receipes')

        
        context = {'receipe': queryset}
        return render (request, 'update_receipe.html', context)
    
    
    
def login_page(request):
    
    if request.method == "POST":
        
        data = request.POST
        
        username = data.get('username')
        password = data.get('password')
        
        # if username does not exits or invalid password
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username.")
            return redirect('/login/')
        
        #authentication checks weather password is of same of username
        user = authenticate(username = username, password = password)
        
        if user is None:
            messages.error(request, "Invalid Password.")
            return redirect('/login/')
        
        else:
            # session maintain of user
            login(request, user)
            return redirect('receipes')


    return render(request, "login.html")





def logout_page(request):
    # logout to remove session method
    logout(request)
    return redirect('/login/')



def register_page(request):
    
    if request.method == "POST":
        
        data = request.POST
        
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        
        
        # if username already present in database
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.info(request, "Username is already taken.")
            return redirect('/register/')
        
        
        # creating a user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        
        
        #Hash password
        user.set_password(password)
        
        # save user in database
        user.save()
        
        messages.success(request, "Account created successfully.")
        return redirect('/login/')
        
    return render(request, "register.html")