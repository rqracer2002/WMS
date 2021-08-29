from django import forms

from .models import Post, Comment, OrderHeader, OrderDetail, BinTransfer,MyModel

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .myscripts import myvalidator


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author','title', 'text',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }


class OrderPickingForm(forms.ModelForm):


    class Meta:
        model = BinTransfer
        fields = ('itemno','srcbin', 'quantitytran',)

        widgets = {
            'itemno': forms.TextInput(attrs={'placeholder': 'ItemNo', 'style': 'width: 300px;', 'class': 'form-control'}),
            'srcbin': forms.TextInput(attrs={'placeholder': 'BinLoc', 'style': 'width: 300px;', 'class': 'form-control'}),
            'quantitytran': forms.TextInput(attrs={'placeholder': 'Quantity', 'style': 'width: 300px;', 'class': 'form-control'})
        }

    def __init__(self,*args,**kwargs):
        super(OrderPickingForm,self).__init__(*args,**kwargs)
        self.fields['itemno'].initial = 'mynameis'



class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class MyModelForm(forms.ModelForm):


    class Meta:
        model = MyModel
        fields = ('upload',)


    # def clean_upload(self):
    #     '''
    #     Check if exists in database.
    #     '''
    #     print("Something stupid")
    #     mymodel_id = self.cleaned_data.get('id')
    #     customvalidator = myvalidator(mymodel_id)
    #     if customvalidator == "valid":
    #         return customvalidator
    #     else:
    #         raise forms.ValidationError('This order already has a POD attached.')
