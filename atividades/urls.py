from django.urls import path
from . import views

app_name = 'atividades' # Define um namespace para suas URLs

urlpatterns = [
    path('', views.select_year, name='select_year'),
    path('<int:year>/', views.select_month, name='select_month'),
    path('<int:year>/<int:month>/', views.calendar_view, name='calendar_view'),
    path('save_activity/', views.save_activity, name='save_activity'), # Para salvar as atividades
]
