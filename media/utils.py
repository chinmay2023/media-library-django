# media/utils.py

EXTENSION_MAP = {
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

def get_guessed_file_type(file_name):
    import os
    ext = os.path.splitext(file_name)[1].lower()
    return EXTENSION_MAP.get(ext), ext
