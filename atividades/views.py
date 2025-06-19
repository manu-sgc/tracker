from django.shortcuts import render, redirect, get_object_or_404
from .models import DailyActivity, DailyTaskItem, DailyTaskCompletion, MediaEntry
from django.http import JsonResponse
import calendar
from datetime import date
from django.db.models import F
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

def daily_tasks_view(request, year, month):
    selected_date = date(year, month, 1) # Usamos o primeiro dia do mês como referência
    
    # Obter todas as tarefas que o usuário definiu (DailyTaskItem)
    all_tasks = DailyTaskItem.objects.all()

    # Obter as conclusões de tarefas para o MÊS selecionado
    # { (task_id, day): completion_object } para fácil acesso
    completed_tasks = {}
    completions_for_month = DailyTaskCompletion.objects.filter(
        date__year=year,
        date__month=month
    ).select_related('task') # Otimiza a busca do objeto TaskItem

    for completion in completions_for_month:
        completed_tasks[(completion.task_id, completion.date.day)] = True
    
    # Gerar os dias do mês
    num_days = calendar.monthrange(year, month)[1] # Número de dias no mês
    days_in_month = [day for day in range(1, num_days + 1)]

    grid_template_columns_str = "200px " + " ".join(["50px"] * num_days)

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        day_to_toggle = int(request.POST.get('day'))
        
        task = get_object_or_404(DailyTaskItem, id=task_id)
        current_date = date(year, month, day_to_toggle)

        # Tentar criar ou deletar a conclusão
        if (task.id, day_to_toggle) in completed_tasks:
            # Se já está completa, desmarcar (deletar a entrada)
            DailyTaskCompletion.objects.filter(task=task, date=current_date).delete()
        else:
            # Se não está completa, marcar (criar uma nova entrada)
            DailyTaskCompletion.objects.create(task=task, date=current_date)
        
        # Redirecionar para a mesma página para atualizar o estado
        return redirect('atividades:daily_tasks', year=year, month=month)

    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'all_tasks': all_tasks,
        'days_in_month': days_in_month,
        'completed_tasks': completed_tasks,
        'current_day': timezone.localdate().day if timezone.localdate().year == year and timezone.localdate().month == month else None
    }
    return render(request, 'atividades/daily_tasks.html', context)

# View para adicionar/gerenciar tarefas rastreáveis (DailyTaskItem)
def manage_tasks(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name').strip()
        if task_name:
            # Tentar criar a tarefa, ignorando se já existir (unique=True)
            DailyTaskItem.objects.get_or_create(name=task_name)
        return redirect('atividades:manage_tasks')
    
    tasks = DailyTaskItem.objects.all()
    context = {
        'tasks': tasks
    }
    return render(request, 'atividades/manage_tasks.html', context)

# View para deletar uma tarefa rastreável
def delete_task(request, task_id):
    task = get_object_or_404(DailyTaskItem, id=task_id)
    if request.method == 'POST':
        task.delete()
    return redirect('atividades:manage_tasks')

def media_list_view(request):
    if request.method == 'POST':
        media_type = request.POST.get('media_type')
        title = request.POST.get('title').strip()
        notes = request.POST.get('notes', '').strip()
        rating = request.POST.get('rating')

        if media_type and title:
            MediaEntry.objects.create(
                media_type=media_type,
                title=title,
                notes=notes,
                rating=int(rating) if rating else None
            )
        return redirect('atividades:media_list')

    media_entries = MediaEntry.objects.all() # Todas as mídias, não por data
    context = {
        'media_entries': media_entries,
        'media_types': MediaEntry.MEDIA_TYPE_CHOICES,
        'rating_choices': MediaEntry.RATING_CHOICES,
    }
    return render(request, 'atividades/media_list.html', context)

# View para deletar uma mídia
def delete_media(request, media_id):
    media = get_object_or_404(MediaEntry, id=media_id)
    if request.method == 'POST':
        media.delete()
    return redirect('atividades:media_list')