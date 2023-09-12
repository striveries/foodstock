from django.db import models

class Items(models.Model):
    item_name = models.CharField(max_length=255)
    amount = models.IntegerField()
    description = models.TextField()