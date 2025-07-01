from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .utils import get_guessed_file_type

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

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
    tags = models.ManyToManyField(Tag, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    size = models.BigIntegerField(null=True, blank=True)
    extension = models.CharField(max_length=10, null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name if self.file else "No file"

    def clean(self):
        if self.file and self.file_type:
            guessed_type, ext = get_guessed_file_type(self.file.name)
            if not guessed_type:
                raise ValidationError(f"Unsupported file extension: '{ext}'.")

            if guessed_type != self.file_type.lower():
                raise ValidationError(
                    f"File type mismatch: you selected '{self.file_type.upper()}', "
                    f"but uploaded a '{ext}' file, which is of type '{guessed_type.upper()}'."
                )
