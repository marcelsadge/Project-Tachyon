from django.db import models

# Create your models here.

class About(models.Model):
    player = models.TextField()
    year = models.TextField()
    type = models.TextField()

    def __str__(self):
        return str(self.player)