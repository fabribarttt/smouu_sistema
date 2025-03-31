from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class Rol(models.Model):
    rol = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.rol


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Ciudades"

    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.IntegerField()
    telefono = PhoneNumberField()
    direccion = models.CharField(max_length=200, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING)
    fecha_contratatacion = models.DateField()
    rol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING)
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="empleado", blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "Empleados"


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.IntegerField()
    ruc = models.IntegerField(blank=True, null=True)
    telefono = PhoneNumberField()
    direccion = models.CharField(max_length=200, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING)
    correo = models.EmailField()


class Dispositivo(models.Model):
    TIPOS_DISPOSITIVO = [
        ("smartphone", "Smartphone"),
        ("tablet", "Tablet"),
        ("wearable", "Reloj"),
        ("notebook", "Notebook"),
        ("speaker", "Speaker"),
    ]

    categoria = models.CharField(max_length=50, choices=TIPOS_DISPOSITIVO)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
