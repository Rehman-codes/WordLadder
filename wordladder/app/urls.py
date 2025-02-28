from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mode/', views.mode, name='mode'),
    path('challenge/', views.challenge, name='challenge'),
    path('play/<int:challenge_id>/', views.playground, name='playground'),
 path('add_word/<int:challenge_id>/', views.add_word, name='add_word'),
]