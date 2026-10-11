from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    # Activity Log URLs
    path('', views.activity_list, name='list'),
    path('add/', views.activity_create, name='create'),
    path('<int:pk>/edit/', views.activity_update, name='update'),
    path('<int:pk>/delete/', views.activity_delete, name='delete'),

    # Badge URLs
    path('badges/', views.badge_list, name='badge_list'),
    path('badges/add/', views.badge_create, name='badge_create'),
    path('badges/award/<int:participant_pk>/', views.award_badge, name='award_badge'),

]