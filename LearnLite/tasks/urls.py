from django.urls import path
from . import views

app_name = "tasks"

urlpatterns  = [
    path('all/', views.all_tasks_view, name='all_tasks_view')
]