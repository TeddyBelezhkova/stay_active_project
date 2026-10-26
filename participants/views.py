from django.shortcuts import render, redirect, get_object_or_404
from .models import Department, Participant
from .forms import DepartmentForm, ParticipantForm
from activities.forms import AwardBadgeForm
from activities.models import Badge, ActivityLog  # <-- Added ActivityLog
from django.db.models import Q, Count, OuterRef, Subquery  # <-- Added OuterRef, Subquery
from django.contrib import messages

#-----------DEPARTMENTS-------------#
def department_list(request):
    # Subquery: Count all activities done by participants belonging to this department
    activity_count_subquery = ActivityLog.objects.filter(
        participant__department=OuterRef('pk')
    ).values('participant__department').annotate(
        total=Count('pk')
    ).values('total')

    # Subquery: Count all participants belonging to this department
    participant_count_subquery = Participant.objects.filter(
        department=OuterRef('pk')
    ).values('department').annotate(
        total=Count('pk')
    ).values('total')

    departments = Department.objects.annotate(
        participant_count=Subquery(participant_count_subquery),
        activity_count=Subquery(activity_count_subquery),
    )
    return render(request, 'participants/department_list.html', {'departments': departments})


def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participants:department_list')
    else:
        form = DepartmentForm()
    return render(request, 'participants/department_form.html', {'form': form, 'title': 'Add Department'})

def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('participants:department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'participants/department_form.html', {'form': form, 'title': 'Edit Department'})

def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('participants:department_list')
    return render(request, 'participants/department_confirm_delete.html', {'department': department})



#-----------PARTICIPANTS-------------#
def participant_list(request):
    search_query = request.GET.get('q', '').strip()
    department_id = request.GET.get('department', '')

    departments = Department.objects.all()
    participants = Participant.objects.select_related('department').all()

    #search filter
    if search_query:
        participants = participants.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    #department filter
    if department_id:
        participants = participants.filter(department_id=department_id)

    context = {
        'participants': participants,
        'departments': departments,
        'search_query': search_query,
        'selected_department': department_id,
    }


    return render(request, 'participants/participant_list.html', context)


def participant_detail(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    activities = participant.activities.all()
    badges = participant.badges.all()

    if request.method == 'POST':
        award_form = AwardBadgeForm(request.POST)
        if award_form.is_valid():
            badge = award_form.cleaned_data['badge']
            if badge in participant.badges.all():
                messages.error(request, f"'{participant.full_name}' already has the {badge.title} badge!")
            else:
                participant.badges.add(badge)
                messages.success(request, f"Awarded '{badge.title}' badge to {participant.full_name}! 🏆")
            return redirect('participants:detail', pk=participant.pk)
    else:
        award_form = AwardBadgeForm()

    context = {
        'participant': participant,
        'activities': activities,
        'badges': badges,
        'award_form': award_form,
    }
    return render(request, 'participants/participant_detail.html', context)


def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            messages.success(request, f"Participant '{participant.full_name}' was created successfully!")
            return redirect('participants:detail', pk=participant.pk)
    else:
        form = ParticipantForm()
    return render(request, 'participants/participant_form.html', {'form': form, 'title': 'Add Participant'})


def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated details for '{participant.full_name}'.")
            return redirect('participants:detail', pk=participant.pk)
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participants/participant_form.html', {'form': form, 'title': 'Edit Participant'})


def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant_name = participant.full_name
        participant.delete()
        messages.info(request, f"Participant '{participant_name}' was deleted.")
        return redirect('participants:list')
    return render(request, 'participants/participant_confirm_delete.html', {'participant': participant})


def revoke_badge(request, participant_pk, badge_pk):
    participant = get_object_or_404(Participant, pk=participant_pk)
    badge = get_object_or_404(Badge, pk=badge_pk)

    if request.method == 'POST':
        participant.badges.remove(badge)
        messages.info(request, f"Badge '{badge.title}' was revoked from {participant.full_name}.")

    return redirect('participants:detail', pk=participant.pk)