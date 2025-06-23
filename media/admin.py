from django.contrib import admin
from .models import Tag, MediaFile, Category

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'file_type', 'owner', 'uploaded_at', 'is_public', 'is_processed')
    list_filter = ('file_type', 'category', 'is_public', 'is_processed')
    search_fields = ('file__name', 'owner__username')
    raw_id_fields = ('owner',)
    filter_horizontal = ('tags',)
