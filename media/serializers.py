from rest_framework import serializers
from .models import MediaFile, Tag, Category
<<<<<<< HEAD
from .utils import get_guessed_file_type
=======
import os

>>>>>>> a664c486631055869c7609f8ed58ad4b7b35d15a

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

<<<<<<< HEAD
=======

>>>>>>> a664c486631055869c7609f8ed58ad4b7b35d15a
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

<<<<<<< HEAD
=======

>>>>>>> a664c486631055869c7609f8ed58ad4b7b35d15a
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
<<<<<<< HEAD
            guessed_type, ext = get_guessed_file_type(file.name)

            if not guessed_type:
                raise serializers.ValidationError({
                    'file': f"Unsupported file extension: '{ext}'"
                })

            if guessed_type != file_type.lower():
                raise serializers.ValidationError({
                    'file_type': f"File type mismatch: uploaded file has extension '.{ext}', but selected file_type is '{file_type}'"
=======
            ext = os.path.splitext(file.name)[1].lower().strip('.')
            extension_map = {
                'jpg': 'image',
                'jpeg': 'image',
                'png': 'image',
                'gif': 'image',
                'mp3': 'audio',
                'wav': 'audio',
                'mp4': 'video',
                'avi': 'video',
                'pdf': 'pdf',
                'doc': 'doc',
                'docx': 'doc',
            }
            guessed_type = extension_map.get(ext)

            if not guessed_type:
                raise serializers.ValidationError({
                    'file': f"Unsupported file extension: .{ext}"
                })

            if guessed_type != file_type.lower().strip():
                raise serializers.ValidationError({
                    'file_type': f"File type mismatch: uploaded file has extension '.{ext}', but file_type is '{file_type}'"
>>>>>>> a664c486631055869c7609f8ed58ad4b7b35d15a
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
