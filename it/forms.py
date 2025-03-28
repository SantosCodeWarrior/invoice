from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'       
    )


class ImageForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'       
    )

class InwardForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'       
    )