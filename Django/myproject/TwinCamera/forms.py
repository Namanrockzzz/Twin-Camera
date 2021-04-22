from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('image',)

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)

        # for example change class for integerPolje1
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['id'] = 'formFile'