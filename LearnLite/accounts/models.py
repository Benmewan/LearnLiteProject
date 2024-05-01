from django import forms
from django.db import models
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class SubscribtionType(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField()
    days = models.IntegerField()
    price = models.FloatField()

    def __str__(self) -> str:
        return self.name

    
class Subsribe(models.Model):
    subscription_type = models.ForeignKey(SubscribtionType, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    subsribe = models.OneToOneField(Subsribe, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    payment_date = models.DateTimeField(auto_now_add=True)
    name_on_card = models.CharField(max_length=100)
    expiry_date = models.CharField(max_length=5)
    cvv_code = models.CharField(max_length=4)



