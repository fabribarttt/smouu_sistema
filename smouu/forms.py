from django import forms
from .models import Cliente


class RegisterClientForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"
        labels = {
            "nombre": "Nombre",
            "apellido": "Apellido",
            "cedula": "Cedula",
            "ruc": "RUC",
            "telefono": "Telefono",
            "direccion": "Direccion",
            "ciudad": "Ciudad",
            "correo": "Correo",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "cedula": forms.TextInput(attrs={"class": "form-control"}),
            "ruc": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "ciudad": forms.Select(attrs={"class": "form-select"}),
            "correo": forms.EmailInput(attrs={"class": "form-control"}),
        }
