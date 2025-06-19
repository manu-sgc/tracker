from django.db import models
from django.utils import timezone

class DailyActivity(models.Model):
    date = models.DateField(unique=True)
    # Humor do dia: 1 (ruim) a 5 (ótimo)
    MOOD_CHOICES = [
        (1, 'Péssimo'),
        (2, 'Ruim'),
        (3, 'Neutro'),
        (4, 'Bom'),
        (5, 'Excelente'),
    ]
    mood_rating = models.IntegerField(choices=MOOD_CHOICES, null=True, blank=True)
    
    # Campo para comentário geral do dia, se ainda quiser mantê-lo aqui
    # Ou pode ser movido para DailyTaskCompletion ou outro lugar se for específico de tarefa
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Activity for {self.date.strftime('%Y-%m-%d')} - Mood: {self.mood_rating}"

    class Meta:
        verbose_name = "Atividade Diária (Humor)"
        verbose_name_plural = "Atividades Diárias (Humor)"
        ordering = ['date']

# Modelo para DEFINIR AS TAREFAS que o usuário quer rastrear (ex: "Beber água")
class DailyTaskItem(models.Model):
    name = models.CharField(max_length=255, unique=True) # Nome da tarefa (ex: "Beber 2L de água")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tarefa Diária a Rastrear"
        verbose_name_plural = "Tarefas Diárias a Rastrear"
        ordering = ['name']

# Modelo para REGISTRAR QUANDO uma tarefa foi completada em um dia específico
class DailyTaskCompletion(models.Model):
    task = models.ForeignKey(DailyTaskItem, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que uma tarefa só pode ser marcada como completa uma vez por dia
        unique_together = ('task', 'date')
        verbose_name = "Conclusão de Tarefa Diária"
        verbose_name_plural = "Conclusões de Tarefas Diárias"
        ordering = ['date', 'task__name'] # Ordena por data e nome da tarefa

# Modelo para mídias (livros, filmes, séries)
class MediaEntry(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('livro', 'Livro'),
        ('filme', 'Filme'),
        ('serie', 'Série'),
    ]
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]

    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_media_type_display()}] {self.title} - {self.rating} estrelas"

    class Meta:
        verbose_name = "Item de Mídia Consumida"
        verbose_name_plural = "Itens de Mídia Consumida"
        ordering = ['-created_at']