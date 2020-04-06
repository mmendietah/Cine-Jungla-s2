from django import forms
from .models import Registrado

class RegModelForm(forms.ModelForm):
    class Meta:
        model = Registrado
        fields = ["nombre", "email"]
    def clean_email(self):
        email = self.cleaned_data.get("email")
        # long = len(clave)
        # if not any(c.isupper() for c in clave):
        #     print("Ingrese una mayúscula.")
        # elif not any(c.islower() for c in clave):
        #     print("Ingrese una minúscula.")
        # elif not any(c.isdigit() for c in clave):
        #     print("Ingrese un número.")
        return email
    # def clean_email(self):
    #     print(self.cleaned_data)
    #     return "email@email.com"
    #     email = self.cleaned_data.get("email")
    #     if not "edu" in email:
    #         raise forms.ValidationError("Educativo")
    #     return email

class RegFrom(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()

class ContactForm(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea)

class CarritoForm(forms.Form):
    nombre = forms.CharField(required=False)
    cantidad = forms.IntegerField()

class PagForm(forms.Form):
    pag = forms.CharField()

class addProd(forms.Form):
    nombre = forms.CharField(required=False)
    cantidad = forms.IntegerField