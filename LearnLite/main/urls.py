from django.urls import path
from . import views

app_name = "main"

urlpatterns  = [
    path("", views.index_view, name="index_view"),
    path("contact/", views.contact_view, name="contact_view"),
    path("about/", views.about_view, name="about_view"),
    path("message/", views.message_view, name="message_view"),
    path("mode/dark/", views.dark_mode_view, name="dark_mode_view"),
    path("mode/light/", views.light_mode_view, name="light_mode_view"),
    path('not_exist/', views.not_exist, name='not_exist'),
]