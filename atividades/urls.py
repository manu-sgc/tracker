from django.urls import path
from . import views
from .views import calendario

urlpatterns = [
    path('', views.tracker_view, name='tracker'),
    path('calendario/', calendario, name='calendario'),
    path('avaliacao/', views.avaliacao_view, name='avaliacao'),
    path('leitura/', views.leitura_view, name='leitura'),
    path('habitos/', views.habitos_view, name='habitos'),
    path('salvar-progresso/', views.salvar_progresso, name='salvar-progresso'),
    path('sono/', views.sono_view, name='sono'),
    path('filmes_series/', views.filmes_series_view, name='filmes_series'),
]
