from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User, Group


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
    rol = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
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

    categoria = models.CharField(
        max_length=50, choices=TIPOS_DISPOSITIVO, default="smartphone"
    )
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)


class OrdenReparacion(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(
        Empleado, on_delete=models.CASCADE, null=True, blank=True
    )
    id_dispositivo = models.ForeignKey(Dispositivo, on_delete=models.DO_NOTHING)
    problema_reportado = models.TextField()
    observaciones = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)


class CategoriaProducto(models.Model):
    nombre_categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_categoria


class Proveedore(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nombre_local = models.CharField(max_length=100)
    contacto = PhoneNumberField()
    tipo_producto = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_local


class InventarioRepuesto(models.Model):
    nombre_repuesto = models.CharField(max_length=100)
    id_categoria = models.ForeignKey(CategoriaProducto, on_delete=models.DO_NOTHING)
    cantidad_disponible = models.IntegerField()
    precio = models.IntegerField()
    id_proveedor = models.ForeignKey(Proveedore, on_delete=models.DO_NOTHING)


class MovimientoRepuesto(models.Model):
    CHOICE = [
        (0, "Salida"),
        (1, "Entrada"),
    ]
    id_repuesto = models.ForeignKey(InventarioRepuesto, on_delete=models.CASCADE)
    tipo_movimiento = models.BooleanField(choices=CHOICE)
    cantidad = models.IntegerField()


class AsignacionReparacion(models.Model):
    ESTADOS = [
        ("pediente", "Pendiente"),
        ("enproceso", "En Proceso"),
        ("terminado", "Terminado"),
    ]
    id_orden = models.ForeignKey(OrdenReparacion, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(
        Empleado, on_delete=models.CASCADE, null=True, blank=True
    )
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    estado_reparacion = models.CharField(
        max_length=30,
        choices=ESTADOS,
        default="pendiente",
    )
