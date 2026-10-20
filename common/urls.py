from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
]