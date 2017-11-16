from django import forms

class LinkConverterForm(forms.Form):
    link = forms.CharField(label='Song or album url', max_length=200)
