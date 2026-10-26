from django.urls import path
from . import views

app_name = 'participants'

urlpatterns = [
    # Department URLS
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_update, name='department_edit' ),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),

    # Participants URLs
    path("", views.participant_list, name='list'),
    path('add/', views.participant_create, name='create'),
    path('<int:pk>/', views.participant_detail, name='detail'),
    path('<int:pk>/edit/', views.participant_update, name='edit'),
    path('<int:pk>/delete/', views.participant_delete, name='delete'),
    path('<int:participant_pk>/badges/<int:badge_pk>/revoke/', views.revoke_badge, name='revoke_badge'),
]