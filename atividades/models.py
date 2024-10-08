from django.db import models

class Dia(models.Model):
    data = models.DateField()
    avaliacao = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    paginas_lidas = models.IntegerField()
    atividades = models.CharField(max_length=255)
    habitos = models.CharField(max_length=255)
    horas_de_sono = models.CharField(max_length=255)
    destaque = models.TextField()
    filmes_series = models.TextField()

class ProgressoHabitual(models.Model):
    dia = models.IntegerField()
    atividade = models.CharField(max_length=100)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.dia} - {self.atividade} - {"Completado" if self.completado else "Não completado"}'
