from django.shortcuts import render
from django.db.models import Count
from activities.models import ActivityLog, Badge
from participants.models import Participant, Department


def home_page(request):

    #participants by earned badges
    leaderboard = Participant.objects.annotate(
        badge_count=Count('badges'),
    ).prefetch_related('badges', 'department').order_by('-badge_count')[:5]

    context = {
        'total_participants': Participant.objects.count(),
        'total_departments': Department.objects.count(),
        'total_activities': ActivityLog.objects.count(),
        'total_badges': Badge.objects.count(),
        'leaderboard': leaderboard,
        'top_performers': Participant.get_top_performers(limit=3),
        'recent_activities': ActivityLog.objects.select_related('participant')[:5],
    }
    return render(request, 'common/home.html', context)

def how_it_works(request):
    #renders the guidelines page
    return render(request, 'common/how_it_works.html')