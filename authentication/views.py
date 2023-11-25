from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password




@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
    

@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
    

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return JsonResponse({'message': 'Username and password are required.'}, status=400)
        
        user = User.objects.create_user(username=username, password=password)
        # Optionally, you can log in the user after registration
        user.save()
        auth_login(request, user)
        return JsonResponse({
            "status": True,
            "message": "Registrasi sukses!"
            # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
        }, status=201)# Redirect to the login page or any other page

    else:
        return JsonResponse({
            "status": False,
            "message": "Registrasi gagal"
        }, status=401)