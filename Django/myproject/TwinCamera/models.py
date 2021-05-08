from django.db import models
from django import forms
from .storage import OverwriteStorage
import os
import uuid
from django.conf import settings

def path_and_rename(instance, filename):
    try:
        os.makedirs(settings.MEDIA_ROOT+'images/'+str(instance.id))
    except:
        pass
    upload_to = 'images/'+str(instance.id)
    ext = filename.split('.')[-1]
    # get filename
    s="unknown"
    if filename==str(instance.bg):
        s='bg'
    elif filename==str(instance.img1):
        s='img1'
    elif filename==str(instance.img2):
        s='img2'
    elif filename==str(instance.img3):
        s='img3'
    elif filename==str(instance.img4):
        s='img4'
    elif filename==str(instance.img5):
        s='img5'
    elif filename==str(instance.img6):
        s='img6'
    
    # set filename as random string
    filename = '{}.{}'.format(s, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

# Create your models here.
class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bg = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    img1 = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    img2 = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    img3 = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    img4 = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    img5 = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    img6 = models.ImageField(upload_to=path_and_rename, null=True, blank=True)