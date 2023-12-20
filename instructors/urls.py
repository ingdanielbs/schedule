from . import views
from django.urls import path

urlpatterns = [      
    path('', views.index_instructors, name='instructors'),
    path('schedule/', views.schedule, name='schedule'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('schedule_down/', views.schedule_down, name='schedule_down_instructor'),       
]