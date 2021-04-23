from django import forms
from .models import Image

n = 1

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
        fields = ('img1','img2','img3','img4','img5','img6')

    def __init__(self, *args, **kwargs):
        super(ImgForm, self).__init__(*args, **kwargs)
        try:
            n = int(args[0]['n'])
            for i in range(n+1,7):
                self.fields.pop('img'+str(i))

            # for example change class for integerPolje1
            for i in range(1,n+1):
                self.fields['img'+str(i)].widget.attrs['class'] = 'form-control'
                self.fields['img'+str(i)].widget.attrs['id'] = 'formFile'
        except:
            pass