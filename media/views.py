import csv
from django.http import HttpResponse, FileResponse, Http404
from rest_framework import viewsets, permissions, filters, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action, api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import MediaFile
from .serializers import MediaFileSerializer
from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated
from .models import Tag
from .serializers import TagSerializer
from rest_framework import viewsets 

class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['file_type', 'category', 'is_processed', 'tags']
    search_fields = ['file']
    ordering_fields = ['uploaded_at']

    def perform_create(self, serializer):
        file_obj = self.request.FILES['file']
        instance = serializer.save(
            owner=self.request.user,
            size=file_obj.size,
            extension=file_obj.name.split('.')[-1].lower()
        )
        try:
            from .tasks import extract_metadata
            extract_metadata.delay(instance.id)
        except Exception as e:
            print("Celery error:", e)
            extract_metadata(instance.id)

    def get_queryset(self):
        return MediaFile.objects.filter(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def export(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="media_files_export.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'ID', 'File Name', 'File Type', 'Size (bytes)', 'Extension',
            'Duration (s)', 'Width', 'Height', 'Page Count',
            'Category', 'Uploaded At', 'Owner', 'Processed'
        ])

        for obj in queryset:
            writer.writerow([
                obj.id,
                obj.file.name,
                obj.file_type,
                obj.size,
                obj.extension,
                obj.duration,
                obj.width,
                obj.height,
                obj.page_count,
                obj.category.name if obj.category else '',
                obj.uploaded_at,
                obj.owner.username,
                obj.is_processed
            ])

        return response

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        try:
            media = self.get_object()
            return FileResponse(media.file.open('rb'), as_attachment=True)
        except Exception as e:
            print("Download error:", e)
            raise Http404("File not found.")

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_download(request, pk):
    media = get_object_or_404(MediaFile, pk=pk, is_public=True)
    try:
        return FileResponse(media.file.open('rb'), as_attachment=True)
    except:
        raise Http404("File not found.")

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]