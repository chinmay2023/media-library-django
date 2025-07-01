<<<<<<< HEAD
from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Tag, MediaFile, Category
from .utils import get_guessed_file_type
=======
from django import forms
from django.contrib import admin
from .models import MediaFile, Tag, Category
import os
from django.core.exceptions import ValidationError
>>>>>>> a664c486631055869c7609f8ed58ad4b7b35d15a


class MediaFileAdminForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = '__all__'

<<<<<<< HEAD
=======
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['file'].required = False
        if 'owner' in self.fields:
            self.fields['owner'].widget = forms.HiddenInput()

>>>>>>> a664c486631055869c7609f8ed58ad4b7b35d15a
    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        file_type = cleaned_data.get('file_type')

        if file and file_type:
<<<<<<< HEAD
            guessed_type, ext = get_guessed_file_type(file.name)

            if not guessed_type:
                raise ValidationError({'file': f"Unsupported file extension: '{ext}'"})

            if guessed_type != file_type.lower():
                raise ValidationError({
                    'file_type': f"File type mismatch: you selected '{file_type.upper()}' "
                                 f"but uploaded a '{ext}' file (type guessed: '{guessed_type.upper()}')."
                })
=======
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
>>>>>>> a664c486631055869c7609f8ed58ad4b7b35d15a

        return cleaned_data


<<<<<<< HEAD
=======
@admin.register(MediaFile)
>>>>>>> a664c486631055869c7609f8ed58ad4b7b35d15a
class MediaFileAdmin(admin.ModelAdmin):
    form = MediaFileAdminForm
    list_display = ('id', 'file', 'file_type', 'owner', 'uploaded_at', 'is_public', 'is_processed')
    list_filter = ('file_type', 'category', 'is_public', 'is_processed')
    search_fields = ('file__name', 'owner__username')
    filter_horizontal = ('tags',)

<<<<<<< HEAD

admin.site.register(MediaFile, MediaFileAdmin)
admin.site.register(Tag)
admin.site.register(Category)
=======
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
>>>>>>> a664c486631055869c7609f8ed58ad4b7b35d15a
