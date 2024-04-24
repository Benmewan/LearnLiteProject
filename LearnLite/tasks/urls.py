from django.urls import path
from . import views

app_name = "tasks"

urlpatterns  = [
    path('all/', views.all_tasks_view, name='all_tasks_view'),
    path('add/', views.add_task_view, name='add_task_view'),
    path('update/task/status/<int:task_id>/', views.update_task_status_view, name='update_task_status_view')
]