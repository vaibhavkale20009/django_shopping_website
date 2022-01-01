from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class items(models.Model):
    name=models.CharField(max_length=40)
    desc=models.CharField(max_length=200)
    price=models.IntegerField()
    category=models.CharField(max_length=50)
    stock=models.IntegerField()
    disc=models.FloatField()
    img=models.ImageField(upload_to='images/')
    offers=models.CharField(max_length=200)
    

class cartdb(models.Model):
    name=models.CharField(max_length=40)
    img=models.ImageField(upload_to='images/')
    price=models.IntegerField()
    username=models.CharField(max_length=20)

