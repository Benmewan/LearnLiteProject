from django.db import models
from django.conf import settings

class Document(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)


class Summary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='summaries', null=True)  # only if business logic allows
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='summaries')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    complexity_level = models.CharField(max_length=15, choices=(('main_points', 'Main Points'), ('detailed', 'Detailed')), default='main_points')
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')), default='pending')
