from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .models import News
from .serializers import NewsSerializer
import cloudinary
import cloudinary.uploader
import base64
 
 
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)
 
 
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
 
        if AdminAuthentication.authenticate(password):
            from django.contrib.auth.models import User
 
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
 
    def create(self, request, *args, **kwargs):
        """Cria notícia, fazendo upload da imagem para o Cloudinary se necessário."""
        data = request.data.copy()
        image = data.get('image')
 
        if image and image.startswith('data:image'):
            try:
                upload_result = cloudinary.uploader.upload(image, folder='paroquia')
                data['image'] = upload_result['secure_url']
            except Exception as e:
                return Response({'error': f'Erro ao fazer upload da imagem: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
 
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
    def perform_destroy(self, instance):
        """Deleta a notícia."""
        instance.delete()