from django.shortcuts import render, redirect
from time import sleep
from threading import Thread
from .forms import BGForm, ImgForm
from myproject.main import start
import myproject.config as config

# Create your views here.
def index(request):
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
    return render(request , 'processing.html', {'progress' :config.progress})
