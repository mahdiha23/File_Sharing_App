
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse , FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings
from .models import Folder
import os


def logout_view(request):
    logout(request)
    return redirect("login")


def login_view(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        password = request.POST["password"]
        user = authenticate(request, phone=phone, password=password)
        if user:
            login(request, user)
            return redirect("home")  
        else:
            return HttpResponse("Invalid credentials")

    return render(request, "login.html")



@login_required(login_url='/login/')
def home(request):
    return render(request ,'home.html')




def download(request, uid):
    if request.method == "POST":
        PASSWORD=Folder.objects.get(uid=uid).password
        user_password = request.POST.get("password")
        if user_password == PASSWORD:  # Validate password
            file_path = os.path.join(settings.MEDIA_ROOT, "zip", f"{uid}.zip")  # Update your file path
            return FileResponse(open(file_path, "rb"), as_attachment=True)
        else:
            return HttpResponse("Incorrect password!", status=403)

    return render(request , 'download.html' , context = {'uid' : uid})
