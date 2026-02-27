from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from base.models import Event, CartModel
from django.contrib import messages  



# -------------------- LOGIN --------------------

def login_(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login_.html', {
                'status': 'Wrong username or password'
            })

    return render(request, 'login_.html', {'login_nav': True})


# -------------------- LOGIN & ADD TO CART --------------------

def login2_(request, pk):
    event = Event.objects.get(id=pk)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('addtocart', pk=pk)
        else:
            return render(request, 'login_.html', {'status': 'Wrong username or password', 'data': event})

    return render(request, 'login_.html', {'data': event})








# -------------------- REGISTER --------------------

def register(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'status': 'Username already exists'
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        return redirect('login_')

    return render(request, 'register.html', {'login_nav': True})


# -------------------- PROFILE --------------------

@login_required(login_url='login_')
def profile(request):

    cartproducts_count = CartModel.objects.filter(user=request.user).count()

    return render(request, 'profile.html', {
        'cartproducts_count': cartproducts_count
    })


# -------------------- LOGOUT --------------------

@login_required(login_url='login_')
def logout_(request):
    logout(request)
    return redirect('login_')


# -------------------- RESET PASSWORD (LOGGED-IN USER) --------------------

@login_required(login_url='login_')
def reset(request):

    cartproducts_count = CartModel.objects.filter(user=request.user).count()

    if request.method == 'POST':

        if 'oldpass' in request.POST:

            oldpass = request.POST.get('oldpass')
            auth_user = authenticate(
                username=request.user.username,
                password=oldpass
            )

            if auth_user:
                return render(request, 'reset.html', {
                    'newpass': True,
                    'cartproducts_count': cartproducts_count
                })
            else:
                return render(request, 'reset.html', {
                    'wrong': True,
                    'cartproducts_count': cartproducts_count
                })

        if 'newpass' in request.POST:

            newpass = request.POST.get('newpass')

            if request.user.check_password(newpass):
                return render(request, 'reset.html', {
                    'same': True,
                    'cartproducts_count': cartproducts_count
                })

            request.user.set_password(newpass)
            request.user.save()

            return redirect('login_')

    return render(request, 'reset.html', {
        'profile_nav': True,
        'cartproducts_count': cartproducts_count
    })


# -------------------- FORGOT PASSWORD --------------------

def forgot(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)
            request.session['fp_user'] = user.username
            return redirect('newpassword')

        except User.DoesNotExist:
            return render(request, 'forgot.html', {
                'error': True
            })

    return render(request, 'forgot.html', {'login_nav': True})


# -------------------- NEW PASSWORD --------------------

def newpassword(request):

    username = request.session.get('fp_user')

    if not username:
        return redirect('forgot')

    user = User.objects.get(username=username)

    if request.method == 'POST':

        newpass = request.POST.get('newpass')

        if user.check_password(newpass):
            return render(request, 'newpassword.html', {
                'error': True
            })

        user.set_password(newpass)
        user.save()

        del request.session['fp_user']

        return redirect('login_')

    return render(request, 'newpassword.html', {'login_nav': True})



















