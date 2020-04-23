from django.contrib import admin
from .models import FirstLevelDecryption,FirstLevelEncryption,DefaultAccount,CustomFieldsForDefaultAccount

# Register your models here.
admin.site.register(FirstLevelDecryption)
admin.site.register(FirstLevelEncryption)
admin.site.register(DefaultAccount)
admin.site.register(CustomFieldsForDefaultAccount)
