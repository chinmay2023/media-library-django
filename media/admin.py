from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Tag, MediaFile, Category
from .utils import get_guessed_file_type


class MediaFileAdminForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        file_type = cleaned_data.get('file_type')

        if file and file_type:
            guessed_type, ext = get_guessed_file_type(file.name)

            if not guessed_type:
                raise ValidationError({'file': f"Unsupported file extension: '{ext}'"})

            if guessed_type != file_type.lower():
                raise ValidationError({
                    'file_type': f"File type mismatch: you selected '{file_type.upper()}' "
                                 f"but uploaded a '{ext}' file (type guessed: '{guessed_type.upper()}')."
                })

        return cleaned_data


class MediaFileAdmin(admin.ModelAdmin):
    form = MediaFileAdminForm
    list_display = ('id', 'file', 'file_type', 'owner', 'uploaded_at', 'is_public', 'is_processed')
    list_filter = ('file_type', 'category', 'is_public', 'is_processed')
    search_fields = ('file__name', 'owner__username')
    filter_horizontal = ('tags',)


admin.site.register(MediaFile, MediaFileAdmin)
admin.site.register(Tag)
admin.site.register(Category)
