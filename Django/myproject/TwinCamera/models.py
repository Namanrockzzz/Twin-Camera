from django.db import models
from django import forms

# Create your models here.
class Image(models.Model):
    bg = models.ImageField(upload_to='images', default="download.png")
    img1 = models.ImageField(upload_to='images', default="download.png")
    img2 = models.ImageField(upload_to='images', default="download.png")
    img3 = models.ImageField(upload_to='images', default="download.png")
    img4 = models.ImageField(upload_to='images', default="download.png")
    img5 = models.ImageField(upload_to='images', default="download.png")
    img6 = models.ImageField(upload_to='images', default="download.png")