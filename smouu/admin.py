from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from .models import (
    Empleado,
    Ciudad,
    CategoriaProducto,
    Proveedore,
    InventarioRepuesto,
    MovimientoRepuesto,
    Servicio,
)

admin.site.site_header = "Smouu Planet"
admin.site.site_title = "Smouu Planet"
admin.site.index_title = "Smouu Planet Administrador"

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
Group._meta.verbose_name_plural = "Roles"
Group._meta.verbose_name = "Rol"


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "apellido",
        "cedula",
        "telefono",
        "rol",
    )


@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ("nombre",)


@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre_categoria",)


@admin.register(Proveedore)
class ProveedoreAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "apellido",
        "nombre_local",
        "contacto",
        "tipo_producto",
    )


@admin.register(InventarioRepuesto)
class InventarioRepuestoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_repuesto",
        "id_categoria",
        "cantidad_disponible",
        "precio",
        "id_proveedor",
    )


@admin.register(MovimientoRepuesto)
class MovimientoRepuestoAdmin(admin.ModelAdmin):
    list_display = ("id_repuesto", "tipo_movimiento", "cantidad")


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("tipo", "dispositivo", "precio")
