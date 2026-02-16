from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .models import Estudiante
from .serializers import EstudianteSerializer


class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username y password son requeridos'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                }
            })
        else:
            return Response({'error': 'Credenciales inválidas'}, status=401)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'success': True})


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'id': request.user.id,
            'username': request.user.username,
        })