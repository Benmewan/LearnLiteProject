from django.db import models

# Create your models here.

class Contact(models.Model):

    name = models.CharField(max_length=2048)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
