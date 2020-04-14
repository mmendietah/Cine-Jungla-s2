from django import forms
from .models import Producto, Venta, Lista, Venta

class addProd(forms.Form):
    nombre = forms.CharField(required=False)
    cantidad = forms.IntegerField

class regFrom(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    mensaje = forms.CharField(max_length=100)

class ProductoForm (forms.ModelForm):

    class Meta:

        model = Producto

        fields = [

            'nom_producto',
            'valor_unitario',
            'cant_producto',
            'imagen_producto',

        ]

        labels = {

            'nom_producto': 'Nombre del Producto',
            'valor_unitario': 'Valor unitario',
            'cant_producto': 'Cantidad del producto',
        }

        widgets = {

            'nom_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'cant_producto': forms.TextInput(attrs={'class': 'form-control'}),
        }

class listarProductoForm(forms.ModelForm):

    class Meta:

        model = Producto

        fields = [

            'nom_producto',
            'valor_unitario',
            'cant_producto',
            'imagen_producto',

        ]

        labels = {

            'nom_producto': 'Nombre del Producto',
            'valor_unitario': 'Valor unitario',
            'cant_producto': 'Cantidad del producto',
        }


class actualizarProductoForm(forms.ModelForm):

    class Meta:

        model = Producto

        fields = [

            'cant_producto',

        ]

class actualizarListaForm(forms.ModelForm):

    class Meta:

        model = Lista

        fields = [

            'cant_producto'

        ]

class VentaForm (forms.ModelForm):

    class Meta:

        model = Venta

        fields = [

            'cant_producto',
            'ced_vendedor',
            'cod_producto',
        ]

        labels = {

            'cant_producto': 'Cantidad producto',
            'ced_vendedor': 'Vendedor',
            'cod_producto': 'Codigo producto'
        }