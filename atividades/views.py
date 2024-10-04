import calendar
from django.shortcuts import render


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
    return render(request, 'atividades/habitos.html')

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