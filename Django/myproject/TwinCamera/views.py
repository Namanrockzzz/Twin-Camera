from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def page2(request):
    return render(request, 'page2.html')

def page3(request):
    n = request.GET['n']
    n = int(n)
    return render(request, 'page3.html', {"n":[i for i in range(1,n+1)]})