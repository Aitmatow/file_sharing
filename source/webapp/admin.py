from django.contrib import admin

# Register your models here.
from webapp.models import File, FilePrivate

admin.site.register(File)
admin.site.register(FilePrivate)