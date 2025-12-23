from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.shortcuts import render
# Create your views here.
def index(request):
    question_list =  Question.objects.order_by('-create_at')
    context = {'question_list' : question_list}
    return render(request,'blog/question_list.html',context)

def detail(request,question_id):
    question = Question.objects.get(id=question_id)
    context = {'question':question}
    return render(request,'blog/question_detail.html',context)