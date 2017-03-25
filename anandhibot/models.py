from __future__ import unicode_literals

from django.db import models

# Create your models here.
# Each model extends models.Model
class User(models.Model): 
    # Simple definition of string field
    uid = models.CharField(max_length=30) 
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    uclass = models.CharField(max_length=30)
    prompt = models.CharField(max_length=50)
    major = models.CharField(max_length=100, blank=True)