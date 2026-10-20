from django.shortcuts import render, redirect, get_object_or_404
from .models import Department, Participant
from .forms import DepartmentForm, ParticipantForm
from activities.forms import AwardBadgeForm


def department_list(request):
    departments = Department.objects.all()
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


def participant_list(request):
    participants = Participant.objects.select_related('department').all()
    return render(request, 'participants/participant_list.html', {'participants': participants})


def participant_detail(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    activities = participant.activities.all()
    badges = participant.badges.all()
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
            return redirect('participants:detail', pk=participant.pk)
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participants/participant_form.html', {'form': form, 'title': 'Edit Participant'})


def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participants:list')
    return render(request, 'participants/participant_confirm_delete.html', {'participant': participant})
