from django.db import transaction
from app_movil_escolar_api.serializers import UserSerializer
from app_movil_escolar_api.models import *
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from django.contrib.auth.models import Group, User


#   LISTAR ADMIN

class AdminAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        admins = Administradores.objects.all()
        data = []

        for admin in admins:
            data.append({
                "id": admin.id,
                "first_name": admin.user.first_name,
                "last_name": admin.user.last_name,
                "email": admin.user.email,
                "telefono": admin.telefono,
                "rfc": admin.rfc,
                "edad": admin.edad,
                "ocupacion": admin.ocupacion,
            })

        return Response(data, 200)



#   CREAR ADMINISTRADOR

class AdminView(generics.CreateAPIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)

        if user.is_valid():
            # Datos base del usuario
            role = request.data.get('rol', 'Administrador')
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']

            # Validar usuario existente
            if User.objects.filter(email=email).exists():
                return Response({"message": f"El usuario {email} ya existe."}, status=400)

            # Crear usuario base
            user = User.objects.create(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=True
            )
            user.set_password(password)
            user.save()

            # Asignar grupo
            group, _ = Group.objects.get_or_create(name=role)
            group.user_set.add(user)

            # Crear perfil administrador
            admin = Administradores.objects.create(
                user=user,
                clave_admin=request.data.get("clave_admin"),
                telefono=request.data.get("telefono"),
                rfc=request.data.get("rfc", "").upper(),
                edad=request.data.get("edad"),
                ocupacion=request.data.get("ocupacion")
            )

            return Response({"admin_created_id": admin.id}, status=201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)



#   CREAR ALUMNO

class AlumnoView(generics.CreateAPIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_data = UserSerializer(data=request.data)

        if user_data.is_valid():
            role = request.data.get('rol', 'Alumno')
            email = request.data['email']
            password = request.data['password']
            first_name = request.data['first_name']
            last_name = request.data['last_name']

            if User.objects.filter(email=email).exists():
                return Response({"message": f"El usuario {email} ya existe."}, status=400)

            user = User.objects.create(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=True
            )
            user.set_password(password)
            user.save()

            group, _ = Group.objects.get_or_create(name=role)
            group.user_set.add(user)

            alumno = Alumnos.objects.create(
                user=user,
                matricula=request.data.get("matricula"),
                fecha_nacimiento=request.data.get("fecha_nacimiento"),
                curp=request.data.get("curp"),
                rfc=request.data.get("rfc", "").upper(),
                edad=request.data.get("edad"),
                telefono=request.data.get("telefono"),
                ocupacion=request.data.get("ocupacion")
            )

            return Response({"alumno_created_id": alumno.id}, status=201)

        return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)



#   LISTAR ALUMNOS

class AlumnoAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        alumnos = Alumnos.objects.all()
        data = []

        for alumno in alumnos:
            data.append({
                "id": alumno.id,
                "first_name": alumno.user.first_name,
                "last_name": alumno.user.last_name,
                "email": alumno.user.email,
                "matricula": alumno.matricula,
                "telefono": alumno.telefono,
                "edad": alumno.edad,
                "ocupacion": alumno.ocupacion,
            })

        return Response(data, 200)


#   CREAR MAESTRO

class MaestroView(generics.CreateAPIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_data = UserSerializer(data=request.data)

        if user_data.is_valid():
            role = request.data.get('rol', 'Maestro')
            email = request.data['email']
            password = request.data['password']
            first_name = request.data['first_name']
            last_name = request.data['last_name']

            if User.objects.filter(email=email).exists():
                return Response({"message": f"El usuario {email} ya existe."}, status=400)

            user = User.objects.create(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=True
            )
            user.set_password(password)
            user.save()

            group, _ = Group.objects.get_or_create(name=role)
            group.user_set.add(user)

            maestro = Maestros.objects.create(
                user=user,
                id_trabajador=request.data.get("id_trabajador"),
                fecha_nacimiento=request.data.get("fecha_nacimiento"),
                telefono=request.data.get("telefono"),
                rfc=request.data.get("rfc", "").upper(),
                cubiculo=request.data.get("cubiculo"),
                area_investigacion=request.data.get("area_investigacion"),
                materias_json=request.data.get("materias_json", [])
            )

            return Response({"maestro_created_id": maestro.id}, status=201)

        return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)


#   LISTAR MAESTROS

class MaestroAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        maestros = Maestros.objects.all()
        data = []

        for maestro in maestros:
            data.append({
                "id": maestro.id,
                "first_name": maestro.user.first_name,
                "last_name": maestro.user.last_name,
                "email": maestro.user.email,
                "id_trabajador": maestro.id_trabajador,
                "telefono": maestro.telefono,
                "cubiculo": maestro.cubiculo,
                "area_investigacion": maestro.area_investigacion,
            })

        return Response(data, 200)
