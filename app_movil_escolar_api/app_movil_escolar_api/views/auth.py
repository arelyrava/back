from django.db.models import *
from app_movil_escolar_api.serializers import *
from app_movil_escolar_api.models import *
from rest_framework import permissions, generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user.is_active:
            roles = user.groups.all()
            role_names = [r.name for r in roles]

            profile = None
            if 'Administrador' in role_names:
                profile = Administradores.objects.filter(user=user).first()
            elif 'Alumno' in role_names:
                profile = Alumnos.objects.filter(user=user).first()
            elif 'Maestro' in role_names:
                profile = Maestros.objects.filter(user=user).first()

            if not profile:
                return Response({'error': 'Perfil no encontrado'}, status=status.HTTP_404_NOT_FOUND)

            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'id': user.pk,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'token': token.key,
                'roles': role_names
            })

        return Response({}, status=status.HTTP_403_FORBIDDEN)


class Logout(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            Token.objects.filter(user=user).delete()
            return Response({'logout': True})
        return Response({'logout': False})
