from django.shortcuts import render, redirect
from time import sleep
from threading import Thread
from .forms import ImageForm

progress = 0
# Create your views here.
def index(request):
    return render(request, 'index.html')

def page2(request):
    if request.method=='POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ImageForm()
    return render(request, 'page2.html',{'form':form})

def page3(request):
    n = request.POST['n']
    print(request.FILES)
    n = int(n)
    if request.method=='POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ImageForm()
    return render(request, 'page3.html', {"n":[i for i in range(1,n+1)], 'form':form})

def processing(request , n=0):
    print(request.FILES)
    if request.method=='POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    t = Thread(target=update_progress)
    t.start()
    return redirect("track_progress")

def update_progress():
    for i in range(1,100):
        sleep(0.5)
        global progress
        progress = i
        print(progress)

def track_progress(request):
    return render(request , 'processing.html', {'progress' :progress})
