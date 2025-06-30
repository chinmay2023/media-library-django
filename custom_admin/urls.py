from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('media-files/', views.media_files_view, name='media_files'),
    path('tags/', views.tags_view, name='tags'),
    path('categories/', views.categories_view, name='categories'),
    path('delete/<path:filename>/', views.delete_file, name='delete_file'),
    path('settings/', views.settings_view, name='settings'),
]
