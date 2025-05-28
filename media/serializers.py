from rest_framework import serializers
from .models import MediaFile, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class MediaFileSerializer(serializers.ModelSerializer):
    # show category details in GET
    category = CategorySerializer(read_only=True)
    # accept category assignment via category_id in POST/PATCH
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = MediaFile
        fields = '__all__'
        read_only_fields = ['owner', 'size', 'extension', 'is_processed']
