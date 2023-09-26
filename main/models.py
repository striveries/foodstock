from django.db import models
from django.contrib.auth.models import User

class Items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)
    amount = models.IntegerField()
    description = models.TextField()
    
class User(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    hobby = models.TextField()
    