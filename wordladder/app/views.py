from django.shortcuts import render, HttpResponse, redirect
from .models import GameSettings

#====================================
# Home View
#====================================
def home(request):
    return render(request, "base.html")

#====================================
# Game Mode Selection View
#====================================
def mode(request):
    if request.method == "POST":
        # Capture the selected difficulty level
        difficulty = request.POST.get("difficulty")
        
        # Save the data to the database
        game_setting = GameSettings.objects.create(game_mode=difficulty)
        
        # Redirect to the challenge page
        return redirect('challenge') 
    
    return render(request, "mode.html")

#====================================
# Challenge View
#====================================
def challenge(request):
    # Fetch the last GameSettings object
    game_setting = GameSettings.objects.last()
    difficulty = game_setting.game_mode if game_setting else "easy"

    if request.method == "POST":
        # Capture the start_word and end_word from the form submission
        start_word = request.POST.get("startWord")
        end_word = request.POST.get("endWord")

        # Save the challenge details in the database
        game_setting.start_word = start_word
        game_setting.end_word = end_word
        game_setting.challenge_type = "predefined"  # as it's selected from predefined challenges
        game_setting.save()

        # Redirect to the playground page
        return redirect(f'/play/{game_setting.id}')

    return render(request, "challenge.html", {'difficulty': difficulty})

#====================================
# Playground View
#====================================
def playground(request, challenge_id):
    # Fetch the challenge details from the database
    challenge = GameSettings.objects.get(id=challenge_id)
    return render(request, "playground.html", {'challenge': challenge})