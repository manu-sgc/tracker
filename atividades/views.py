from django.shortcuts import render, redirect, get_object_or_404
from .models import DailyActivity
from django.http import JsonResponse
import calendar
from datetime import date

# 1. Página para escolher o ano
def select_year(request):
    years = [2024, 2025, 2026]
    return render(request, 'atividades/select_year.html', {'years': years})

# 2. Página para escolher o mês
def select_month(request, year):
    months = [
        {'id': 1, 'name': 'Janeiro'}, {'id': 2, 'name': 'Fevereiro'},
        {'id': 3, 'name': 'Março'}, {'id': 4, 'name': 'Abril'},
        {'id': 5, 'name': 'Maio'}, {'id': 6, 'name': 'Junho'},
        {'id': 7, 'name': 'Julho'}, {'id': 8, 'name': 'Agosto'},
        {'id': 9, 'name': 'Setembro'}, {'id': 10, 'name': 'Outubro'},
        {'id': 11, 'name': 'Novembro'}, {'id': 12, 'name': 'Dezembro'},
    ]
    return render(request, 'atividades/select_month.html', {'year': year, 'months': months})

# 3. Página do calendário com marcações
def calendar_view(request, year, month):
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)

    # Obter atividades existentes para o mês/ano
    atividades = DailyActivity.objects.filter(
        date__year=year,
        date__month=month
    ).values('date', 'comment')

    # Criar um dicionário para acesso rápido às atividades por data
    atividades_dict = {activity['date']: activity['comment'] for activity in atividades}

    # Estruturar os dias para o template
    calendar_days = []
    for week in month_days:
        week_data = []
        for day in week:
            if day == 0: # Dias que não pertencem ao mês
                week_data.append({'day': '', 'has_activity': False, 'comment': ''})
            else:
                current_date = date(year, month, day)
                has_activity = current_date in atividades_dict
                comment = atividades_dict.get(current_date, '')
                week_data.append({
                    'day': day,
                    'date': current_date.isoformat(), # Formato YYYY-MM-DD
                    'has_activity': has_activity,
                    'comment': comment
                })
        calendar_days.append(week_data)

    month_name = calendar.month_name[month]

    context = {
        'year': year,
        'month': month,
        'month_name': month_name,
        'calendar_days': calendar_days,
    }
    return render(request, 'atividades/calendar_view.html', context)

# View para salvar a atividade via AJAX
def save_activity(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        comment = request.POST.get('comment', '').strip()

        try:
            activity_date = date.fromisoformat(date_str)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Data inválida.'}, status=400)

        if comment:
            # Atualiza ou cria a atividade com o comentário
            DailyActivity.objects.update_or_create(
                date=activity_date,
                defaults={'comment': comment}
            )
            return JsonResponse({'status': 'success', 'message': 'Comentário salvo com sucesso.'})
        else:
            # Se o comentário estiver vazio, remove a atividade para a data
            DailyActivity.objects.filter(date=activity_date).delete()
            return JsonResponse({'status': 'success', 'message': 'Comentário removido.'})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)