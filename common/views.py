from django.shortcuts import render
from django.db.models import Count
from activities.models import ActivityLog, Badge
from participants.models import Participant, Department


def home_page(request):
    # Participants by earned badges
    leaderboard = Participant.objects.annotate(
        badge_count=Count('badges'),
    ).prefetch_related('badges', 'department').order_by('-badge_count')[:5]

    # Target through model from Badge where the M2M field is defined:
    total_awarded_badges = Badge.participants.through.objects.count()

    context = {
        'total_participants': Participant.objects.count(),
        'total_departments': Department.objects.count(),
        'total_activities': ActivityLog.objects.count(),
        'total_badges': total_awarded_badges,
        'leaderboard': leaderboard,
        'top_performers': Participant.get_top_performers(limit=3) if hasattr(Participant, 'get_top_performers') else [],
        'recent_activities': ActivityLog.objects.select_related('participant')[:5],
    }
    return render(request, 'common/home.html', context)

def how_it_works(request):
    return render(request, 'common/how_it_works.html')