from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('upload/', views.add_test, name='add_test'),
    path('test/<int:test_id>/', views.view_generated_test, name='view_generated_test'),
    path('save/<int:test_id>/', views.save_test, name='save_test'),
    path('test/<int:test_id>/submit/', views.submit_test, name='submit_test'),
    path('test/result/<int:test_id>/', views.test_result, name='test_result'), 
    path('discard/<int:test_id>/', views.discard_test, name='discard_test'),
    path('all/', views.all_tests, name='all_tests'),
]
