from django.contrib import admin
# media/admin.py
from .models import Tag, MediaFile, Category
admin.site.register(Tag)
admin.site.register(MediaFile)
admin.site.register(Category)
