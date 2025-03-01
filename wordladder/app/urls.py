from django.urls import path
from . import views
from .views import playground, set_ai_hint, get_ai_hint

urlpatterns = [
    path('', views.home, name='home'),
    path('mode/', views.mode, name='mode'),
    path('challenge/', views.challenge, name='challenge'),
    path('play/<int:challenge_id>/', views.playground, name='playground'),
    path('add_word/<int:challenge_id>/', views.add_word, name='add_word'),
    path("set-ai-hint/<int:challenge_id>/", set_ai_hint, name="set_ai_hint"),
    path("get-hint/<int:challenge_id>/", get_ai_hint, name="get_ai_hint"),
]