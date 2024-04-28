# admin.py
from django.contrib import admin
from .models import GeneratedTest, Question

admin.site.register(GeneratedTest)
admin.site.register(Question)
