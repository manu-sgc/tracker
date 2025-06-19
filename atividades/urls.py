from django.urls import path
from . import views

app_name = 'atividades' # Define um namespace para suas URLs

urlpatterns = [
    path('select_year/', views.select_year, name='select_year'),
    path('<int:year>/', views.select_month, name='select_month'),
    path('<int:year>/<int:month>/', views.calendar_view, name='calendar_view'),
    path('save_daily_activity/', views.save_daily_activity, name='save_daily_activity'), 
    path('<int:year>/<int:month>/tasks/', views.daily_tasks_view, name='daily_tasks'),
    path('manage_tasks/', views.manage_tasks, name='manage_tasks'),
    path('manage_tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('media/', views.media_list_view, name='media_list'),
    path('media/delete/<int:media_id>/', views.delete_media, name='delete_media'),
]
