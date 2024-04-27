from django.db import models
from django.conf import settings

class TestDocument(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='test_documents/')
    upload_date = models.DateTimeField(auto_now_add=True)

class GeneratedTest(models.Model):
    document = models.ForeignKey(TestDocument, on_delete=models.CASCADE, related_name='tests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()

class Question(models.Model):
    test = models.ForeignKey(GeneratedTest, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=1024)
    choice_a = models.CharField(max_length=255)
    choice_b = models.CharField(max_length=255)
    choice_c = models.CharField(max_length=255)
    choice_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], default='a')
