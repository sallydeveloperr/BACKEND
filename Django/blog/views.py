from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse('<h1>안녕하세요 blog 입니다</h1>')
