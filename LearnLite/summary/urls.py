from django.urls import path
from . import views

app_name = "summary"

urlpatterns = [
    path('add-summary/', views.add_summary, name='add_summary'),
    path('display-summary/<int:summary_id>/', views.display_summary, name='display_summary'),
    path('summaries/', views.list_summaries, name='list_summaries'),
]
