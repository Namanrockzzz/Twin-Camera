from django.db import models
from django import forms

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images')