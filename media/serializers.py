from rest_framework import serializers
from .models import MediaFile, Tag, Category
from .utils import get_guessed_file_type

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

    def validate(self, data):
        file = data.get('file')
        file_type = data.get('file_type')

        if file and file_type:
            guessed_type, ext = get_guessed_file_type(file.name)

            if not guessed_type:
                raise serializers.ValidationError({
                    'file': f"Unsupported file extension: '{ext}'"
                })

            if guessed_type != file_type.lower():
                raise serializers.ValidationError({
                    'file_type': f"File type mismatch: uploaded file has extension '.{ext}', but selected file_type is '{file_type}'"
                })

        return data

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
