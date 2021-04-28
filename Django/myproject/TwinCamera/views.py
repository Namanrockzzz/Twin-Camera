from django.shortcuts import render, redirect
from time import sleep
from threading import Thread
from .forms import BGForm, ImgForm
from myproject.main import start
import myproject.config as config
from django.conf import settings
from .functions import empty_media_folder

# Create your views here.
def index(request):
    empty_media_folder()
    return render(request, 'index.html')

def page2(request):
    if request.method=='POST':
        form = BGForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = BGForm()
    return render(request, 'page2.html',{'form':form})

def page3(request):
    n = request.POST['n']
    print(request.FILES)
    n = int(n)
    if n>6 or n<1:
        return redirect("page2")
    if request.method=='POST':
        form = BGForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = BGForm()
    return render(request, 'page3.html', {'n':n, 'form':ImgForm(request.POST,request.FILES)})

def processing(request , n):
    print(request.FILES)
    if request.method=='POST':
        form = ImgForm(request.POST,request.FILES)
        print(form.is_valid())
        if form.is_valid():
            form.save()
    t = Thread(target=start)
    t.start() 
    return redirect("track_progress")

def track_progress(request):
    if config.progress==100 :
        print(str(settings.MEDIA_ROOT)+"/images/final.jpg")
        return render(request, 'download.html' , {'download':str(settings.MEDIA_ROOT)+"/images/final.jpg"})
    return render(request , 'processing.html', {'progress' :round(config.progress,2)})
