from django.http import HttpResponse
from django.shortcuts import render
import json

def hello(request):
    return render(request,'index.html')

def page_1(request):
    return render(request,'page_1.html')

def page_2(request):
    return render(request,'page_2.html')

def page_3(request):
    return render(request,'page_3.html')