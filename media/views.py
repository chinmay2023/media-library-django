import csv
from django.http import HttpResponse
from rest_framework import viewsets, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from .models import MediaFile
from .serializers import MediaFileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse, Http404



class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['file_type', 'category', 'is_processed']
    search_fields = ['file']
    ordering_fields = ['uploaded_at']

    def perform_create(self, serializer):
        file_obj = self.request.FILES['file']
        instance = serializer.save(
            owner=self.request.user,
            size=file_obj.size,
            extension=file_obj.name.split('.')[-1].lower()
        )

        # Safe trigger for Celery
        try:
            from .tasks import extract_metadata
            extract_metadata.delay(instance.id)
        except Exception as e:
            print("Celery error:", e)
            # Optional: directly run the task instead
            from .tasks import extract_metadata
            extract_metadata(instance.id)


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


    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        try:
            media = self.get_object()
            return FileResponse(media.file.open('rb'), as_attachment=True)
        except Exception as e:
            print("Download error:", e)
            raise Http404("File not found.")

    def get_queryset(self):
        user = self.request.user
        return MediaFile.objects.filter(owner=user)

        return response
