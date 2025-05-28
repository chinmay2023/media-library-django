from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MediaFile(models.Model):
    FILE_TYPES = [
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('doc', 'Document'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    size = models.BigIntegerField(null=True, blank=True)
    extension = models.CharField(max_length=10, null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name

#http://127.0.0.1:8000/api/mediafiles/7/

#{
  #"file_type" : "image",
 # "category_id" : 7

#}
