from django.contrib import admin
from .models import Empleado, Ciudad, Rol

admin.site.site_header = 'Smouu Planet'
admin.site.site_title = 'Smouu Planet'
admin.site.index_title = 'Smouu Planet Administrador'

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'telefono', 'rol',)
   
    
@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('rol', 'descripcion',)