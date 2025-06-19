from django.db import models
from django.utils import timezone

class DailyActivity(models.Model):
    date = models.DateField(unique=True)
    comment = models.TextField(blank=True, null=True)
    # Você pode adicionar mais campos aqui, como tipo de atividade, status, etc.

    def __str__(self):
        return f"Activity for {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Atividade Diária"
        verbose_name_plural = "Atividades Diárias"
        ordering = ['date'] # Ordena as atividades por data