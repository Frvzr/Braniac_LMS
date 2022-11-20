from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('courses/', views.CoursesListView.as_view(), name='courses'),
    path('doc_site/', views.DocSiteView.as_view(), name='doc_site'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('news/', views.NewsView.as_view(), name='news'),
    # path('news/<int:page>/', views.NewsWithPaginatorView.as_view(), name = "news_paginator"),
    path('news/<int:pk>/', views.NewsDetail.as_view(), name='news_detail'),
    path('courses/<int:pk>', views.CoursesDetail.as_view(), name='courses_detail'),
    
]
