from django.shortcuts import render, redirect, get_object_or_404
from .models import ActivityLog, Badge, ActivityComment, ActivityReaction
from .forms import ActivityLogForm, BadgeForm, AwardBadgeForm, CommentForm
from participants.models import Participant
from django.db.models import Count, Q

# Activity Log Views
def activity_list(request):
    search_query = request.GET.get('q', '').strip()
    activity_type = request.GET.get('type', '')

    activities = ActivityLog.objects.select_related('participant').all()

    if search_query:
        activities = activities.filter(
            Q(notes__icontains=search_query) |
            Q(participant__first_name__icontains=search_query) |
            Q(participant__last_name__icontains=search_query)
        )

    if activity_type:
        activities = activities.filter(activity_type=activity_type)

    activity_type_choices = ActivityLog.ACTIVITY_TYPES if hasattr(ActivityLog, 'ACTIVITY_TYPES') else ActivityLog._meta.get_field('activity_type').choices

    context = {
        'activities': activities,
        'search_query': search_query,
        'selected_type': activity_type,
        'activity_types': activity_type_choices,
    }
    return render(request, 'activities/activity_list.html', context)

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

    # counts for each reaction type
    public_logs = public_logs.annotate(
        like_count=Count('reactions', filter=Q(reactions__reaction_type='like')),
        fire_count=Count('reactions', filter=Q(reactions__reaction_type='fire')),
        clap_count=Count('reactions', filter=Q(reactions__reaction_type='clap')),
        trophy_count=Count('reactions', filter=Q(reactions__reaction_type='trophy')),
    )

    return render(request, 'activities/fame_board.html', {'logs': public_logs})


def add_comment(request, pk):
    activity = get_object_or_404(ActivityLog, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.activity = activity  # attach target ActivityLog instance before saving
            comment.save()

    # Always redirect back to the photo card anchor
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(f"{referer}#{pk}")
    return redirect('activities:fame_board')


def add_reaction(request, pk):
    activity = get_object_or_404(ActivityLog, pk=pk)
    if request.method == 'POST':
        reaction_type = request.POST.get('reaction_type')

        #session key as user identifier
        user_id = request.session.session_key or request.META.get('REMOTE_USER', 'anonymous')

        if not request.session.session_key:
            request.session.create()
            user_id = request.session.session_key

        existing_reaction = ActivityReaction.objects.filter(
            activity=activity,
            reaction_type=reaction_type,
            user_identifier=user_id
        ).first()

        if existing_reaction:
            existing_reaction.delete()
        else:
            ActivityReaction.objects.create(
                activity=activity,
                reaction_type=reaction_type,
                user_identifier=user_id,
            )

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(f"{referer}#{pk}")
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

def badge_update(request, pk):
    badge = get_object_or_404(Badge, pk=pk)
    if request.method == 'POST':
        form = BadgeForm(request.POST, instance=badge)
        if form.is_valid():
            form.save()
            return redirect('activities:badge_list')
    else:
        form = BadgeForm(instance=badge)
        return render(request, 'activities/badge_form.html', {'form': form, 'title': 'Edit Badge'})

def badge_delete(request, pk):
    badge = get_object_or_404(Badge, pk=pk)
    if request.method == 'POST':
        badge.delete()
        return redirect('activities:badge_list')
    return render(request, 'activities/badge_confirm_delete.html', {'badge': badge})



def award_badge(request, participant_pk):
    participant = get_object_or_404(Participant, pk=participant_pk)
    if request.method == 'POST':
        form = AwardBadgeForm(request.POST)
        if form.is_valid():
            badge = form.cleaned_data['badge']
            badge.participants.add(participant)
            return redirect('participants:detail', pk=participant.pk)
    return redirect('participants:detail', pk=participant.pk)

