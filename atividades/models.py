from django.db import models
from django.utils import timezone

class DailyActivity(models.Model):
    date = models.DateField(unique=True)
    MOOD_CHOICES = [
        (1, 'Péssimo'),
        (2, 'Ruim'),
        (3, 'Neutro'),
        (4, 'Bom'),
        (5, 'Excelente'),
    ]
    mood_rating = models.IntegerField(choices=MOOD_CHOICES, null=True, blank=True)
    
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Activity for {self.date.strftime('%Y-%m-%d')} - Mood: {self.mood_rating}"

    class Meta:
        verbose_name = "Atividade Diária (Humor)"
        verbose_name_plural = "Atividades Diárias (Humor)"
        ordering = ['date']