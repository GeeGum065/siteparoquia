from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .models import News
from .serializers import NewsSerializer


class AdminAuthentication:
    """Autenticação customizada baseada em senha."""
    
    @staticmethod
    def authenticate(password):
        """Verifica se a senha está correta."""
        return password == settings.ADMIN_PASSWORD


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        """Define permissões por ação."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Endpoint de login customizado."""
        password = request.data.get('password')
        
        if not password:
            return Response({'error': 'Senha é obrigatória.'}, status=status.HTTP_400_BAD_REQUEST)
        
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Senha recebida: '{password}' | Senha esperada: '{settings.ADMIN_PASSWORD}'")
        
        if AdminAuthentication.authenticate(password):
            # Gerar um usuário fake ou usar o admin padrão para gerar token
            from django.contrib.auth.models import User
            
            # Tenta pegar o primeiro superuser ou cria um
            try:
                user = User.objects.filter(is_superuser=True).first()
                if not user:
                    user = User.objects.create_superuser('admin', 'admin@paroquia.local', settings.ADMIN_PASSWORD)
            except:
                user = User.objects.filter(is_superuser=True).first()
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Senha incorreta.'}, status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        """Salva a notícia."""
        serializer.save()

    def perform_destroy(self, instance):
        """Deleta a notícia."""
        instance.delete()
