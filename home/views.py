from django.shortcuts import render,redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



# id=pppp pass: smit@@93
# ssss   wwww@@##

#signup page 

def signupUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        
        # validations
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('/signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('/signup')

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()
       

        messages.success(request, "Account created successfully. Please login.")
       

        return redirect('/login')

    return render(request, 'signup.html')


def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
        
    return render(request, 'index.html')

def shop(request):
    return render(request, 'shop.html')

def deals(request):
    return render(request, 'deals.html')

def contact(request):   # small letter
    if request.method == "POST":
         #context 
        # context = {
        #         'name': request.user.username,
        #         'email': request.user.email,
        #     }
        context = {
                'name': request.session.get('username'),
                'email': request.session.get('email'),
            }

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact_data = Contact(
            name=name,
            email=email,
            message=message,
            date=datetime.today()
        )
        contact_data.save()

        

        messages.success(request, "Your Message is Successfully sent")
        context = {
            'name': request.session.get('username'),
            'email': request.session.get('email'),
        }


    #  ALWAYS return HttpResponse
    return render(request, 'contact.html')

def loginUser(request):
    if request.method=="POST":
         username=request.POST.get('username')
         password = request.POST.get('password')
        # if user login with true createtial
         user = authenticate(username=username, password=password)
         
       
                
         if user is not None:
            login(request, user)
            messages.success(request, f"successfully login as {username}")

           
            return redirect('/')
         else:
            messages.error(request, "Invalid username or password")
            return redirect('/login')
            

        
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    messages.get_messages(request).used = True
    messages.success(request, "Logged out successfully")

    return redirect('/login')


#profile 

# @login_required(login_url='/login/')
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})








