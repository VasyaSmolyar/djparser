from django.db import models
from django.utils import timezone

# Create your models here.
class Site(models.Model):
    url = models.CharField(max_length=255)
    query = models.CharField(max_length=255)
    pub_date = models.DateTimeField(default=timezone.now)

class Node(models.Model):
    site = models.ForeignKey(Site,on_delete=models.CASCADE)
    val = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
