from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        try:
            s = (name.split(".")[0]).split("\\")[-1]+"."
            path = str(settings.MEDIA_ROOT)[:-1]+"\\"+name.split("\\")[0]+"\\"
            for i in os.listdir(path):
                if path+i and s in i:
                    os.remove(path+i)
        except:
            s = (name.split(".")[0]).split("/")[-1]+"."
            path = str(settings.MEDIA_ROOT)[:-1]+"/"+name.split("/")[0]+"/"
            for i in os.listdir(path):
                if path+i and s in i:
                    os.remove(path+i)
        # If the filename already exists, remove it as if it was a true file system
        return name