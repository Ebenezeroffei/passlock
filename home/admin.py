from django.contrib import admin
from .models import FirstLevelDecryption,FirstLevelEncryption,DefaultAccount

# Register your models here.
admin.site.register(FirstLevelDecryption)
admin.site.register(FirstLevelEncryption)
admin.site.register(DefaultAccount)
