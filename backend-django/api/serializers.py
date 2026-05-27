from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    image = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = News
        fields = ['id', 'titulo', 'categoria', 'data', 'texto', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']
