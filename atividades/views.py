import calendar
from django.shortcuts import render

import numpy as np
import matplotlib.pyplot as plt
from django.http import HttpResponse
from io import BytesIO

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import ProgressoHabitual


def tracker_view(request):
    return render(request, 'atividades/tracker.html')

def avaliacao_view(request):
    dias_do_mes = list(range(1, 32))  # Cria uma lista de 1 a 31
    return render(request, 'atividades/avaliacao.html', {'dias_do_mes': dias_do_mes})

def leitura_view(request):
    return render(request, 'atividades/leitura.html')

def atividades_view(request):
    return render(request, 'atividades/adulting.html')

def habitos_view(request):
    dias = list(range(1, 32))  # Dias de 1 a 31
    atividades = list(range(1, 9))  # Atividades de 1 a 8
    positions = []

    for dia in dias:
        for atividade in atividades:
            x = 50 + (dia - 1) * 35  # Posição x para cada dia
            y = 50 + (atividade - 1) * 35  # Posição y para cada atividade
            positions.append((x, y, dia, atividade))  # Adiciona a tupla (x, y, dia, atividade)

    context = {
        'positions': positions
    }
    
    return render(request, 'atividades/habitos.html', context)

def sono_view(request):
    return render(request, 'atividades/sono.html')

def destaque_view(request):
    return render(request, 'atividades/destaque.html')

def filmes_series_view(request):
    return render(request, 'atividades/filmes_series.html')

def calendario(request):
    # Cria uma lista para o calendário
    month = 10  # Outubro
    year = 2024  # Altere para o ano atual ou desejado
    cal = calendar.monthcalendar(year, month)

    return render(request, 'atividades/calendario.html', {'calendar': cal})

def salvar_progresso(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dia = data.get('dia')
        atividade = data.get('atividade')
        completado = data.get('completado')

        progresso, created = ProgressoHabitual.objects.update_or_create(
            dia=dia, atividade=atividade,
            defaults={'completado': completado}
        )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)