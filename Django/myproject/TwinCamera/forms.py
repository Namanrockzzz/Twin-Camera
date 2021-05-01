from django import forms
from .models import Image
       
class ImgForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('bg','img1','img2','img3','img4','img5','img6')

    def __init__(self, *args, **kwargs):
        super(ImgForm, self).__init__(*args, **kwargs)

        self.fields['bg'].required = True
        self.fields['img1'].required = True
        self.fields['bg'].widget.attrs['class'] = 'form-control'
        self.fields['bg'].widget.attrs['id'] = 'formFile'
        self.fields['bg'].label = "Background Image"
        for i in range(1,7):
            self.fields['img'+str(i)].widget.attrs['class'] = 'form-control'
            self.fields['img'+str(i)].widget.attrs['id'] = 'formFile'
            self.fields['img'+str(i)].label = "Image "+str(i)