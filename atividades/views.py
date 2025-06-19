from django.shortcuts import render, redirect, get_object_or_404
from .models import DailyActivity
from django.http import JsonResponse
import calendar
from datetime import date
from django.utils import timezone

def select_year(request):
    years = [2024, 2025, 2026]
    return render(request, 'atividades/select_year.html', {'years': years})

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

def calendar_view(request, year, month):
    cal = calendar.Calendar(firstweekday=6) # 6 para Domingo
    month_days = cal.monthdayscalendar(year, month)

    # Obter atividades existentes para o mês/ano
    atividades = DailyActivity.objects.filter(
        date__year=year,
        date__month=month
    ).values('date', 'mood_rating', 'comment') # Buscar mood_rating e comment

    # Criar um dicionário para acesso rápido às atividades por data
    atividades_dict = {activity['date']: {'mood_rating': activity['mood_rating'], 'comment': activity['comment']} for activity in atividades}

    # Estruturar os dias para o template
    calendar_days = []
    for week in month_days:
        week_data = []
        for day in week:
            if day == 0: # Dias que não pertencem ao mês
                week_data.append({'day': '', 'date': '', 'mood_rating': None, 'comment': ''})
            else:
                current_date = date(year, month, day)
                activity_data = atividades_dict.get(current_date, {'mood_rating': None, 'comment': ''})
                week_data.append({
                    'day': day,
                    'date': current_date.isoformat(), # Formato ISO: YYYY-MM-DD
                    'mood_rating': activity_data['mood_rating'],
                    'comment': activity_data['comment']
                })
        calendar_days.append(week_data)

    month_name = calendar.month_name[month]

    context = {
        'year': year,
        'month': month,
        'month_name': month_name,
        'calendar_days': calendar_days,
        'weekdays': ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
        'mood_choices': DailyActivity.MOOD_CHOICES # Passa as opções de humor para o JS
    }
    return render(request, 'atividades/calendar_view.html', context)

# View para salvar o humor do dia e comentário via AJAX
def save_daily_activity(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        mood_rating = request.POST.get('mood_rating')
        comment = request.POST.get('comment', '').strip()

        try:
            activity_date = date.fromisoformat(date_str)
            mood_rating = int(mood_rating) if mood_rating else None
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Dados inválidos.'}, status=400)

        # Usar get_or_create para garantir que a DailyActivity exista
        activity, created = DailyActivity.objects.get_or_create(date=activity_date)
        activity.mood_rating = mood_rating
        activity.comment = comment
        activity.save()
        
        return JsonResponse({'status': 'success', 'message': 'Humor e comentário salvos com sucesso.', 'mood_rating': mood_rating})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)