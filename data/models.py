from django import template
from django.db import models
from django.contrib.auth.models import User

domain = template.Library()

# Account model for user accounts
class Account(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Stores images created by training on data set into an Images model
class Images(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.TextField(null=True)
    date1 = models.TextField(null=True)
    date2 = models.TextField(null=True)
    type = models.TextField(null=True)
    pitches = models.TextField(null = True)
    img = models.TextField(null = True)
    timestamp = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def get_author(self):
        self.user.username

    def get_name(self):
        if self.account is None:
            return "User"
        return self.account.name
