from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('page2/', views.page2, name='page2'),
    path('processing/', views.processing , name ='processing'),
    path('download/<id>', views.download , name='download'),
    path('track_progress/<id>', views.track_progress, name="track_progress"),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]+staticfiles_urlpatterns()