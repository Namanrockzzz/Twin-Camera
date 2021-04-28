import os
from django.conf import settings

def empty_media_folder():
    dir = str(settings.MEDIA_ROOT)+"/images/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))