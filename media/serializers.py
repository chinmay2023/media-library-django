from rest_framework import serializers
from .models import MediaFile, Tag, Category

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class MediaFileSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )

    class Meta:
        model = MediaFile
        fields = '__all__'
        read_only_fields = ['owner', 'size', 'extension', 'is_processed']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        media = super().create(validated_data)
        self._handle_tags(media, tags_data)
        return media

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        self._handle_tags(instance, tags_data)
        return instance

    def _handle_tags(self, media, tags_data):
        for tag in tags_data:
            tag_obj, _ = Tag.objects.get_or_create(name=tag['name'])
            media.tags.add(tag_obj)
