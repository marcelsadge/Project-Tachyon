from django.db import models

# Create your models here.

class BaseballData(models.Model):
	name = models.CharField(max_length=200)
