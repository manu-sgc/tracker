from django.urls import path
from . import views

urlpatterns = [
    path('', views.tracker_view, name='tracker'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('avaliacao/', views.avaliacao_view, name='avaliacao'),
    path('leitura/', views.leitura_view, name='leitura'),
    path('adulting/', views.atividades_view, name='adulting'),
    path('habitos/', views.habitos_view, name='habitos'),
    path('sono/', views.sono_view, name='sono'),
    path('destaque/', views.destaque_view, name='destaque'),
    path('filmes_series/', views.filmes_series_view, name='filmes_series'),
]
