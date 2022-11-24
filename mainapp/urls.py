from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

    path('doc_site/', views.DocSiteView.as_view(), name='doc_site'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    # News
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/add/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/detail/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    # Courses
    path('courses/', views.CoursesListView.as_view(), name='course'),
    path('courses/<int:pk>/detail/',
         views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/feedback/',
         views.CourseFeedbackCreateView.as_view(), name='course_feedback'),
]
