from django.shortcuts import render
from time import sleep

# Create your views here.
def index(request):
    return render(request, 'index.html')

def page2(request):
    return render(request, 'page2.html')

def page3(request):
    n = request.GET['n']
    n = int(n)
    return render(request, 'page3.html', {"n":[i for i in range(1,n+1)]})

def processing(request , n=10):
    return update_progress(request , 5, n)

def update_progress(request, i, n):
    return render(request , 'processing.html' , {'progress' : i/n*100})
