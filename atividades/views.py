from django.shortcuts import render

def tracker_view(request):
    return render(request, 'atividades/tracker.html')

def avaliacao_view(request):
    return render(request, 'atividades/avaliacao.html')

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

def calendario_view(request):
    return render(request, 'atividades/calendario.html')
