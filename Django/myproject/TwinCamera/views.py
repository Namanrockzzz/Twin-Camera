from django.shortcuts import render, redirect
from django.http import JsonResponse
from time import sleep
from threading import Thread
from .forms import BGForm, ImgForm
from myproject.main import start
import myproject.config as config
from django.conf import settings
from .functions import empty_media_folder
from .models import Image

# Create your views here.
def index(request):
    print(request.session.session_key)
    if not request.session.exists(request.session.session_key):
        request.session.create()
    return render(request, 'index.html')

def page2(request):
    Image.objects.all().delete()
    empty_media_folder()
    form = BGForm()
    return render(request, 'page2.html',{'form':form})

def page3(request):
    n = request.POST['n']
    print(request.FILES)
    n = int(n)
    if request.method=='POST':
        form = BGForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        else :
            return redirect("page2")
    else:
        form = BGForm()
    return render(request, 'page3.html', {'n':n, 'form':ImgForm(request.POST,request.FILES)})

def processing(request):
    print(request.FILES)
    if request.method=='POST':
        form = ImgForm(request.POST,request.FILES)
        form.instance.sid = request.session
        print(form.is_valid())
        if form.is_valid():
            form.save()
        else:
            return redirect("page3")
    config.process = 0
    t = Thread(target=start)
    t.start() 
    return render(request , 'processing.html')

def track_progress(request):
    return JsonResponse({'progress' :round(config.progress,2)} , status= 200)

def download(request):
    return render(request , "download.html")
