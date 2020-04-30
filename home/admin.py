from django.contrib import admin
from .models import FirstLevelDecryption,FirstLevelEncryption,Account,CustomFieldsForAccount

# Register your models here.
admin.site.register(FirstLevelDecryption)
admin.site.register(FirstLevelEncryption)
admin.site.register(Account)
admin.site.register(CustomFieldsForAccount)
