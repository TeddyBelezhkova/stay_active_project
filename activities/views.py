from django.shortcuts import render, redirect, get_object_or_404
from .models import ActivityLog, Badge, ActivityComment, ActivityReaction
from .forms import ActivityLogForm, BadgeForm, AwardBadgeForm
from participants.models import Participant

# Activity Log Views
def activity_list(request):
    activities = ActivityLog.objects.select_related('participant').all()
    return render(request, 'activities/activity_list.html', {'activities': activities})


def activity_create(request):
    if request.method == 'POST':
        form = ActivityLogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('activities:list')
    else:
        form = ActivityLogForm()
    return render(request, 'activities/activity_form.html', {'form': form, 'title': 'Log Workout'})


def activity_update(request, pk):
    activity = get_object_or_404(ActivityLog, pk=pk)
    if request.method == 'POST':
        form = ActivityLogForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activities:list')
    else:
        form = ActivityLogForm(instance=activity)
    return render(request, 'activities/activity_form.html', {'form': form, 'title': 'Edit Workout Log'})


def activity_delete(request, pk):
    activity = get_object_or_404(ActivityLog, pk=pk)
    if request.method == 'POST':
        activity.delete()
        return redirect('activities:list')
    return render(request, 'activities/activity_confirm_delete.html', {'activity': activity})

# Fame Board Views
# public workout logs with proof photos, comments, and reactions
def fame_board(request):
    public_logs = ActivityLog.objects.filter(
        proof_photo__isnull=False,
        is_private=False
    ).exclude(proof_photo='').select_related('participant').prefetch_related('comments', 'reactions')

    return render(request, 'activities/fame_board.html', {'logs': public_logs})


def add_comment(request, pk):
    activity = get_object_or_404(ActivityLog, pk=pk)
    if request.method == 'POST':
        author_name = request.POST.get('author_name', 'Anonymous')
        content = request.POST.get('content')
        if content:
            ActivityComment.objects.create(
                activity=activity,
                author_name=author_name,
                content=content,
            )
    return redirect('activities:fame_board')

def add_reaction(request, pk):
    activity = get_object_or_404(ActivityLog, pk=pk)
    if request.method == 'POST':
        reaction_type = request.POST.get('reaction_type', 'like')
        ActivityReaction.objects.create(
            activity=activity,
            reaction_type=reaction_type,
        )
    return redirect('activities:fame_board')

# Badge Views
def badge_list(request):
    badges = Badge.objects.prefetch_related('participants').all()
    return render(request, 'activities/badge_list.html', {'badges': badges})

def badge_create(request):
    if request.method == 'POST':
        form = BadgeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('activities:badge_list')
    else:
        form = BadgeForm()
    return render(request, 'activities/badge_form.html', {'form': form, 'title': 'Create New Badge'})

def award_badge(request, participant_pk):
    participant = get_object_or_404(Participant, pk=participant_pk)
    form = AwardBadgeForm(request.POST)
    if form.is_valid():
        badge = form.cleaned_data['badge']
        badge.participants.add(participant)
        return redirect('participants:detail', pk=participant.pk)
    return redirect('participants:detail', pk=participant.pk)

