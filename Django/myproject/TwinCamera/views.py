from django.shortcuts import render, redirect
from django.http import JsonResponse
from time import sleep
from threading import Thread
from .forms import ImgForm
from .main import start
from django.conf import settings
from .functions import empty_media_folder
from .models import Image

name = None

# Create your views here.
def index(request):
    # print(request.session.session_key)
    # if not request.session.exists(request.session.session_key):
    #     request.session.create()
    return render(request, 'index.html')

def page2(request):
    # Image.objects.all().delete()
    # empty_media_folder()
    form = ImgForm()
    return render(request, 'page2.html',{'form':form})

# def page3(request):
#     n = request.POST['n']
#     print(request.FILES)
#     n = int(n)
#     if request.method=='POST':
#         form = BGForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#         else :
#             return redirect("page2")
#     else:
#         form = BGForm()
#     return render(request, 'page3.html', {'form':ImgForm(request.POST,request.FILES)})

def processing(request,*args,**kwargs):
    global name
    print(request.FILES)
    if request.method=='POST':
        form = ImgForm(request.POST,request.FILES)
        print(form.is_valid())
        if form.is_valid():
            job = form.save()
            name = job.id
        else:
            return redirect("page2")
    t = Thread(target=start, args=(job.id,))
    t.start() 
    return render(request , 'processing.html', {"name":str(name)})

def track_progress(request,*args,**kwargs):
    f = open(settings.MEDIA_ROOT+"/images/"+str(name)+"/progress.txt","r")
    progress = float(f.readline())
    f.close()
    return JsonResponse({'progress' :round(progress,2)} , status= 200)

def download(request,*args,**kwargs):
    global name
    return render(request , "download.html",{'name':name})
