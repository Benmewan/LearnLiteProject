from django.db import models
from django.conf import settings

class Document(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)

class Summary(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='summaries')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
