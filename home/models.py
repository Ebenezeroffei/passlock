from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import datetime

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
	
	
class Account(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	account_name = models.CharField(max_length = 100)
	date_created = models.DateTimeField(default = timezone.now)
	date_modified = models.DateTimeField(default = timezone.now)
	
	def get_absolute_url(self):
		return reverse('passlock:account_detail',kwargs = {'pk':self.pk})
	
	
	def __str__(self):
		return f"{self.account_name.capitalize()} Account"
	
class CustomFieldsForAccount(models.Model):
	account = models.ForeignKey(Account,on_delete=models.CASCADE)
	field_name = models.CharField(max_length = 100)
	field_type = models.CharField(max_length = 100)
	field_value = models.CharField(max_length = 100)
	
	def __str__(self):
		return f"{self.account.account_name}'s > {self.field_name}"
	