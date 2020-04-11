from django import forms

class addProd(forms.Form):
    nombre = forms.CharField(required=False)
    cantidad = forms.IntegerField

class regFrom(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    mensaje = forms.CharField(max_length=100)