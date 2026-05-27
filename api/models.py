from django.db import models


class News(models.Model):
    CATEGORIES = [
        ('Evento', 'Evento'),
        ('Pastoral', 'Pastoral'),
        ('Comunidade', 'Comunidade'),
        ('Aviso', 'Aviso'),
        ('Liturgia', 'Liturgia'),
    ]

    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=50, choices=CATEGORIES, default='Evento')
    data = models.DateField()
    texto = models.TextField(blank=True)
    image = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data', '-created_at']
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'

    def __str__(self):
        return self.titulo
