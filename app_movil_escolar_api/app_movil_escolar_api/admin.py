from django.contrib import admin
from app_movil_escolar_api.models import Administradores, Alumnos, Maestros


# Administradores

@admin.register(Administradores)
class AdministradoresAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "clave_admin", "telefono", "rfc", "edad", "ocupacion", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name", "rfc")


# Alumnos

@admin.register(Alumnos)
class AlumnosAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "matricula", "curp", "rfc", "edad", "telefono", "ocupacion", "fecha_nacimiento", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name", "matricula", "rfc", "curp")


# Maestros

@admin.register(Maestros)
class MaestrosAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "id_trabajador", "telefono", "rfc", "cubiculo", "area_investigacion", "materias_json", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name", "id_trabajador", "rfc")
