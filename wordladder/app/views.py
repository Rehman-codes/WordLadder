from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import GameSettings
from django.contrib import messages
import requests
from .utilities.pathfinding import find_next_word

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
        difficulty = request.POST.get("difficulty")
        game_setting = GameSettings.objects.create(game_mode=difficulty)
        return redirect('challenge') 
    return render(request, "mode.html")

#====================================
# Challenge View
#====================================
def challenge(request):
    game_setting = GameSettings.objects.last()
    difficulty = game_setting.game_mode if game_setting else "easy"

    if request.method == "POST":
        start_word = request.POST.get("startWord")
        end_word = request.POST.get("endWord")

        game_setting.start_word = start_word
        game_setting.end_word = end_word
        game_setting.challenge_type = "predefined"
        game_setting.ladder = [start_word]  # ✅ Initialize ladder with start word
        game_setting.current_word = start_word  # ✅ Set current_word at start
        game_setting.current_moves = 0  # ✅ Reset move count
        game_setting.save()

        return redirect('playground', challenge_id=game_setting.id)

    return render(request, "challenge.html", {'difficulty': difficulty})

#====================================
# Playground View
#====================================
def playground(request, challenge_id):
    challenge = get_object_or_404(GameSettings, id=challenge_id)
    ladder = challenge.ladder if challenge.ladder else []
    words_reversed = list(reversed(ladder))
    return render(request, "playground.html", {'challenge': challenge, 'words_reversed': words_reversed})

#====================================
# Validation Functions
#====================================
def is_valid_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        data = response.json()
        return isinstance(data, list) and bool(data)
    except Exception as e:
        print(f"Error validating word: {e}")
        return False

def is_word_length_valid(new_word, start_word, end_word):
    return len(new_word) == len(start_word) == len(end_word)

def is_one_letter_changed(new_word, previous_word):
    if not previous_word:
        return True  
    new_word, previous_word = new_word.strip().lower(), previous_word.strip().lower()
    return sum(1 for a, b in zip(new_word, previous_word) if a != b) == 1  

#====================================
# Add Word Function
#====================================
def add_word(request, challenge_id):
    if request.method == "POST":
        challenge = get_object_or_404(GameSettings, id=challenge_id)
        new_word = request.POST.get("new_word").strip().lower()

        if not is_valid_word(new_word):
            messages.error(request, "The word is not a valid English word.")
        elif not is_word_length_valid(new_word, challenge.start_word, challenge.end_word):
            messages.error(request, "Unmatched word length.")
        else:
            previous_word = challenge.ladder[-1] if challenge.ladder else challenge.start_word
            if not is_one_letter_changed(new_word, previous_word):
                messages.error(request, "You can only change one letter at a time.")
            else:
                if not challenge.ladder:
                    challenge.ladder = []
                challenge.ladder.append(new_word)
                challenge.current_word = new_word  # ✅ Update current word
                challenge.current_moves += 1  # ✅ Increase move count
                
                # ✅ Check for victory
                if new_word == challenge.end_word:
                    challenge.victory = True
                    messages.success(request, "🎉 Congratulations! You've completed the challenge!")

                challenge.save()

        return redirect('playground', challenge_id=challenge.id)
    return redirect('home')

#====================================
# AI Hint Functions
#====================================
def set_ai_hint(request, challenge_id):
    challenge = get_object_or_404(GameSettings, id=challenge_id)
    if request.method == "POST":
        selected_hint = request.POST.get("ai_hint")
        if selected_hint in dict(GameSettings.AI_HINTS):
            challenge.ai_hint = selected_hint
            challenge.save()
    return redirect("playground", challenge_id=challenge.id)

def get_ai_hint(request, challenge_id):
    challenge = get_object_or_404(GameSettings, id=challenge_id)
    next_word = None
    if challenge.ai_hint:
        next_word = find_next_word(challenge.game_mode, challenge.current_word, challenge.end_word, challenge.ai_hint)

    words_reversed = list(reversed(challenge.ladder))  # ✅ Preserve ladder state
    return render(request, "playground.html", {"challenge": challenge, "next_word": next_word, "words_reversed": words_reversed})
