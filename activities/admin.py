from django.contrib import admin

from activities.models import Badge, ActivityLog


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('title', 'criteria')
    search_fields = ('title', 'criteria')
    filter_horizontal = ('participants',) # Provides a dual-list box for awarding badges

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('participant', 'activity_type', 'distance_km', 'activity_date')
    list_filter = ('activity_type', 'activity_date', 'participant__department')
    search_fields = ('participant__first_name', 'participant__last_name', 'notes')
    date_hierarchy = 'activity_date'