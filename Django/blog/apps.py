from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

'''
# 장고 프로젝트 생성
django-admin startproject mysite
django-admin startapp blog

# setting.py
INSTALLED_APPS = [
***
'blog.apps.BlogConfig',
]

TEMPLATES = [
    {
...
'DIRS': [BASE_DIR / 'templates'],
...
]

python manage.py makemigration
python manage.py migrate

# templates 폴더 생성 BASE_DIR 위치에  이 위치는 db.sqlite3가 있는곳
templates/blog 폴더 생성
폴더에 question_detail.html   question.list.html 작성

url path를 각 app로 위임
mysite/urls.py  

from django.urls import path, include
path('blog/', include('blog.urls') ),

blog 폴더에  urls.py 파일 생성

from django.urls import path
from . import views
urlpatterns = [    
    path('', views.index),   # http://127.0.0.1:8000/blog/
    path('<int:question_id>/', views.detail)
]

model 생성

amdin.py에는 편하게 사용하기 위해서  관리자 페이지에서 추가삭제 하도록

from .models import Question, Answer
# Register your models here.
admin.site.register(Question)
admin.site.register(Answer) 



그리고 관리자페이지는
python manage.py createsuperuser
'''