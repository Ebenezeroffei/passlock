# Imports
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
import string



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
	field_type_choices = (
		('password','Password'),
		('text','Text'),
		('email','Email'),
		('number','Number'),
	)
	account = models.ForeignKey(Account,on_delete=models.CASCADE)
	field_name = models.CharField(max_length = 100)
	field_type = models.CharField(max_length = 100,choices = field_type_choices)
	field_value = models.CharField(max_length = 100)
	
	def save(self):
		if self.field_type.lower() == 'password':
			encryption = Encryption(self.field_value)
			self.field_value = encryption.encrypt()
		super().save()
		
	def decrypt_password(self):
		if self.field_type == 'password':
			decryption = Decryption(self.field_value)
			return decryption.decrypt()
	
	def __str__(self):
		return f"{self.account.account_name}'s > {self.field_name}"
	
class Encryption:
    """ This class contains algorithms that will encrypt a user's password """
    
    def __init__(self,password):
        self.password = password
    
    def level_one_encryption(self):
        """ This is the first level in the enryption process where every single character of the password is replaced with four characters """
        level_one_encryption_data = ''
        # Goes through every character
        for char in self.password:
            encryption_data = get_object_or_404(FirstLevelEncryption,key = char) # Gets the four characters to replace the character
            level_one_encryption_data += encryption_data.value # Create an encrypted data
            
        return level_one_encryption_data
        
    def level_two_encryption(self,password):
        """  This is the second stage of the encryption process where each character is the changed to a different character using an algorithm """
        level_two_encryption_data = ''
        # Get all the printable characters and remove unwanted ones
        modified_string = string.printable.strip()
        # A list with an equal length with the number of printable characters
        virtual_lst = list(range(len(modified_string)))
        # Goes through every index of the printable characters
        for index in range(len(modified_string)):
            # Sends the position of the index forward thrice
            # Insert the new index of the character in the list
            if index - 3 < 0:
                new_index = len(modified_string) + (index - 3)
                virtual_lst[new_index] = modified_string[index]
            else:
                new_index = index - 3
                virtual_lst[new_index] = modified_string[index]
                
        # Goes through every character in the password
        for char in password:
            # Finds its corresponding character to create another encrypted
            # password
            index_in_modified_string = modified_string.find(char)
            level_two_encryption_data += virtual_lst[index_in_modified_string]
            
        return level_two_encryption_data
            
        
    def level_three_encryption(self,password):
        """ This is the third and last level in the encryption stage """
        virtual_lst = list(password) # Makes a list from the password
        virtual_lst.reverse() # Reverses it
        # Form a new password
        level_three_encryption_data = ''.join(virtual_lst) 
        return level_three_encryption_data
    
    def encrypt(self):
        """ This method is responsible for creating a new password by going
            through all the three stages of encryption"""
        level_one = self.level_one_encryption() # Level one
        level_two = self.level_two_encryption(level_one) # Level two
        
        return self.level_three_encryption(level_two) # Level three
        
                
        
class Decryption:
    """ This class contains algorithms that will decrypt a user's password """
    
    def __init__(self,password):
        self.password = password
    
    def level_one_decryption(self):
        """ This method is the first level in the decryption stage """
        virtual_lst = list(self.password) # Makes a list from the password
        virtual_lst.reverse() # Reverses it
        # Formrs a new password
        level_one_decryption_data = ''.join(virtual_lst)
        return level_one_decryption_data
    
    def level_two_decryption(self,password):
        """ This is the second stage in the decryption process where the method changes
            every character to a different character generated by an algorithn"""
        level_two_decryption_data = ''
        # Get all the printable characters and remove unwanted ones
        modified_string = string.printable.strip()
        # A list with the same lenght as the number of printable characters
        virtual_lst = list(range(len(modified_string)))
        # Goes through every index of the printable character 
        for index in range(len(modified_string)):
            # Sends the index back three times
            # Replace new index of the character in the list
            if index + 3 > len(modified_string) - 1:
                new_index = (index + 3) - (len(modified_string))
                virtual_lst[new_index] = modified_string[index]
            else:
                new_index = index + 3
                virtual_lst[new_index] = modified_string[index]
                
        # Goes through every character in the string 
        for char in password:
            # Use the character's index  to find it's corresponding character
            index_in_modified_string = modified_string.find(char)
            # Form a new decrypted word
            level_two_decryption_data += virtual_lst[index_in_modified_string]
        return level_two_decryption_data
        
    def level_three_decryption(self,password):
        """ This is the second stage in the decryption process where the method changes
            every four sets of character to its corresponding character"""
        level_three_decryption_data = ''
         # Goes through every four characters of the password  
        for char in range(0,len(password) + 1,4):
            if char - 4 >= 0:
                key = password[char - 4:char]
                # Gets its corresponding character
                decryption_data = get_object_or_404(FirstLevelDecryption,key = key)
                # Form a decrypted word
                level_three_decryption_data += decryption_data.value
				
        return level_three_decryption_data 
    
    def decrypt(self):
        """ This method goes through all the three levels in decrypting a password """
        level_one = self.level_one_decryption() # Level one
        level_two = self.level_two_decryption(level_one) # Level two
        return self.level_three_decryption(level_two) # Level three

	