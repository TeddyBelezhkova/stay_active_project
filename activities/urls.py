from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    # Activity Log URLs
    path('', views.activity_list, name='list'),
    path('add/', views.activity_create, name='create'),
    path('<int:pk>/edit/', views.activity_update, name='update'),
    path('<int:pk>/delete/', views.activity_delete, name='delete'),

    # Fame Board URLs
    path('fame-board/', views.fame_board, name='fame_board'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/react/', views.add_reaction, name='add_reaction'),

    # Badge URLs
    path('badges/', views.badge_list, name='badge_list'),
    path('badges/add/', views.badge_create, name='badge_create'),
    path('badges/award/<int:participant_pk>/', views.award_badge, name='award_badge'),

]