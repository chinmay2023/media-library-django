from django import forms
from django.contrib import admin
from .models import MediaFile, Tag, Category
import os
from django.core.exceptions import ValidationError


class MediaFileAdminForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['file'].required = False
        if 'owner' in self.fields:
            self.fields['owner'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        file_type = cleaned_data.get('file_type')

        if file and file_type:
            ext = os.path.splitext(file.name)[1].lower()
            extension_map = {
                '.jpg': 'image',
                '.jpeg': 'image',
                '.png': 'image',
                '.gif': 'image',
                '.mp3': 'audio',
                '.wav': 'audio',
                '.mp4': 'video',
                '.avi': 'video',
                '.pdf': 'pdf',
                '.doc': 'doc',
                '.docx': 'doc',
            }

            guessed_type = extension_map.get(ext)

            if not guessed_type:
                self.add_error('file', f"Unsupported file extension: '{ext}'")
                return cleaned_data

            if guessed_type != file_type.lower():
                self.add_error(
                    'file_type',
                    f"File type mismatch: you selected '{file_type.upper()}' but uploaded a '{ext}' file."
                )

        return cleaned_data


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    form = MediaFileAdminForm
    list_display = ('id', 'file', 'file_type', 'owner', 'uploaded_at', 'is_public', 'is_processed')
    list_filter = ('file_type', 'category', 'is_public', 'is_processed')
    search_fields = ('file__name', 'owner__username')
    filter_horizontal = ('tags',)

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)