from . import views
from django.urls import path

urlpatterns = [      
    path('', views.index_courses, name='courses'),
    path('course_schedule/', views.schedule, name='course_schedule'), 
    path('course_schedule_down/', views.schedule_down, name='course_schedule_down'),   
    path('upload_students/', views.uploadStudents, name='upload_students'),
    path('upload_competences/', views.uploadCompetences, name='upload_competences'),
    path('complaints/', views.complaints, name='complaints'),
]