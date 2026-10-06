from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden

def home(request):
    return HttpResponse("<h1>Welcome to my Django Webpage!</h1>")

def about(request):
    context = {
        'app':'Firstapp',
        'Version':2.0
    }
    return render(request, 'about.html', context)

def greet(request, name):
    return HttpResponse(f'<h2>Hello {name}!</h2>') 
