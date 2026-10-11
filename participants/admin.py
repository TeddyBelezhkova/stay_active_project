from django.contrib import admin

from participants.models import Department, Participant


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'email', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name', 'last_name')
