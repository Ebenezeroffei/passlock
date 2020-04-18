from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class FirstLevelEncryption(models.Model):
    key = models.CharField(max_length = 1)
    value = models.CharField(max_length = 4)
    
    def __str__(self):
        return self.key
    
class FirstLevelDecryption(models.Model):
    key = models.CharField(max_length = 4)
    value = models.CharField(max_length = 1)
    
    def __str__(self):
        return self.key
    
class DefaultAccount(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    account_name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 200)
    date_created = models.DateTimeField(default = timezone.now)
    date_modified = models.DateTimeField(default = timezone.now)
    
    def __str__(self):
        return f"Default {self.account_name.capitalize()} Account"