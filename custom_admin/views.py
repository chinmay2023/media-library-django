from collections import defaultdict
from django.apps import apps
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote as urlunquote
from django.views.decorators.csrf import csrf_protect

from media.models import MediaFile


@csrf_protect
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('custom_admin:custom_admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'custom_admin/login.html', {'dashboard': False})


@login_required
def custom_logout(request):
    logout(request)
    return redirect('custom_admin:custom_login')


@login_required
@csrf_protect
def custom_admin_dashboard(request):
    if request.method == 'POST':
        if request.FILES.get('file'):
            uploaded_file = request.FILES['file']
            MediaFile.objects.create(file=uploaded_file, owner=request.user)
            messages.success(request, 'File uploaded successfully.')
            return redirect('custom_admin:custom_admin_dashboard')

        file_id = request.POST.get('file_id')
        if file_id:
            media_file = get_object_or_404(MediaFile, id=file_id)
            media_file.file.delete(save=False)
            media_file.delete()
            messages.success(request, "File deleted successfully.")
            return redirect('custom_admin:custom_admin_dashboard')

    media_files = MediaFile.objects.all()

    # 🔹 Group models by app
    grouped_models = defaultdict(list)
    all_models = apps.get_models()
    for model in all_models:
        app_label = model._meta.app_label.replace("_", " ").title()
        model_name = model._meta.model_name
        verbose_name = model._meta.verbose_name_plural.title()
        grouped_models[app_label].append({
            'name': verbose_name,
            'url': f"/{app_label.lower()}/{model_name}/"  # Modify if needed
        })

    return render(request, 'custom_admin/login.html', {
        'dashboard': True,
        'media_files': media_files,
        'grouped_models': dict(grouped_models)
    })


@login_required
def settings_view(request):
    return render(request, 'custom_admin/setting.html')


@login_required
def delete_file(request, filename):
    decoded_filename = urlunquote(filename)
    file_path = os.path.join(settings.MEDIA_ROOT, decoded_filename)
    if os.path.isfile(file_path) and os.path.commonpath([file_path, settings.MEDIA_ROOT]) == settings.MEDIA_ROOT:
        os.remove(file_path)
        MediaFile.objects.filter(file=decoded_filename).delete()
        messages.success(request, f"'{decoded_filename}' has been deleted.")
    else:
        messages.error(request, f"File '{decoded_filename}' not found or invalid path.")
    return redirect('custom_admin:custom_admin_dashboard')
