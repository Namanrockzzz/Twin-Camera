from django.db import models
from django import forms
from .storage import OverwriteStorage
import os
from uuid import uuid4


def path_and_rename(instance, filename):
    upload_to = 'images'
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
    bg = models.ImageField(upload_to=path_and_rename, default="download.png", storage=OverwriteStorage())
    img1 = models.ImageField(upload_to=path_and_rename, default="download.png", storage=OverwriteStorage())
    img2 = models.ImageField(upload_to=path_and_rename, default="download.png", storage=OverwriteStorage())
    img3 = models.ImageField(upload_to=path_and_rename, default="download.png", storage=OverwriteStorage())
    img4 = models.ImageField(upload_to=path_and_rename, default="download.png", storage=OverwriteStorage())
    img5 = models.ImageField(upload_to=path_and_rename, default="download.png", storage=OverwriteStorage())
    img6 = models.ImageField(upload_to=path_and_rename, default="download.png", storage=OverwriteStorage())