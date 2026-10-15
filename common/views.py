from django.shortcuts import render

from activities.models import ActivityLog, Badge
from participants.models import Participant, Department


def home_page(request):
    context = {
        'total_participants': Participant.objects.count(),
        'total_departments': Department.objects.count(),
        'total_activities': ActivityLog.objects.count(),
        'total_badges': Badge.objects.count(),
        'top_performers': Participant.get_top_performers(limit=3),
        'recent_activities': ActivityLog.objects.select_related('participant')[:5],
    }
    return render(request, 'common/home.html', context)
