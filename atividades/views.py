from django.shortcuts import render

def tracker_view(request):
    return render(request, 'atividades/tracker.html')
