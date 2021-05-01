from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('page2/', views.page2, name='page2'),
    path('processing/', views.processing , name ='processing'),
    path('download/<id>', views.download , name='download'),
    path('track_progress/<id>', views.track_progress, name="track_progress")
]