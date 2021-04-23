from django import forms
from .models import Image
from django_globals import globals as global_req


class BGForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('bg',)

    def __init__(self, *args, **kwargs):
        super(BGForm, self).__init__(*args, **kwargs)

        # for example change class for integerPolje1
        self.fields['bg'].widget.attrs['class'] = 'form-control'
        self.fields['bg'].widget.attrs['id'] = 'formFile'

class ImgForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('img1','img2','img3','img4','img5','img6')[:self.n]

    def __init__(self, *args, **kwargs):
        super(ImgForm, self).__init__(*args, **kwargs)
        self.n = kwargs.pop('n')

        # for example change class for integerPolje1
        for i in range(1,n+1):
            self.fields['img'+str(i)].widget.attrs['class'] = 'form-control'
            self.fields['img'+str(i)].widget.attrs['id'] = 'formFile'