from django.urls import path
from . import views

app_name = "tasks"

urlpatterns  = [
    path('all/', views.all_tasks_view, name='all_tasks_view'),
    path('add/', views.add_task_view, name='add_task_view'),
    path('update/task/<int:task_id>/status/', views.update_task_status_view, name='update_task_status_view'),
    path('task/<int:task_id>/delete', views.delete_task_view, name='delete_task_view'),
    path('edit/<task_id>/task', views.edit_task_view, name='edit_task_view')
]