from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from app_movil_escolar_api.views import bootstrap
from app_movil_escolar_api.views import users
from app_movil_escolar_api.views import auth
from app_movil_escolar_api.views import users

urlpatterns = [
    #Create Admin
        path('admin/', users.AdminView.as_view()),
    #Admin Data
        path('lista-admins/', users.AdminAll.as_view()),
    #Edit Admin
        #path('admins-edit/', users.AdminsViewEdit.as_view())

   # Alumnos
    path('alumno/', users.AlumnoView.as_view()),          # Registrar nuevo alumno
    path('lista-alumnos/', users.AlumnoAll.as_view()),    # Lista de alumnos

    # Maestros
    path('maestro/', users.MaestroView.as_view()),       # Registrar nuevo maestro
    path('lista-maestros/', users.MaestroAll.as_view()), # Lista de maestros
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
