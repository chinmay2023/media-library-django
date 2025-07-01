from celery import shared_task
from .models import MediaFile
import os
from PIL import Image
import subprocess
from PyPDF2 import PdfReader

@shared_task
def extract_metadata(mediafile_id):
    try:
        media = MediaFile.objects.get(id=mediafile_id)
        filepath = media.file.path
        ext = media.extension.lower()

        if ext in ['jpg', 'jpeg', 'png']:
            try:
                img = Image.open(filepath)
                media.width, media.height = img.size
            except Exception as e:
                print(f"[Image error] {filepath}: {e}")

        elif ext in ['mp4', 'mkv', 'mp3', 'wav']:
            try:
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                    'default=noprint_wrappers=1:nokey=1', filepath],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                media.duration = float(result.stdout.decode().strip())
            except Exception as e:
                print(f"[FFProbe error] {filepath}: {e}")

        elif ext == 'pdf':
            try:
                with open(filepath, 'rb') as f:
                    reader = PdfReader(f)
                    media.page_count = len(reader.pages)
            except Exception as e:
                print(f"[PDF error] {filepath}: {e}")

        media.is_processed = True
        media.save()

<<<<<<< HEAD
=======
    except MediaFile.DoesNotExist:
        print(f"[Metadata task error] MediaFile with id {mediafile_id} does not exist.")
>>>>>>> a664c486631055869c7609f8ed58ad4b7b35d15a
    except Exception as e:
        print("[Metadata task error]", e)
