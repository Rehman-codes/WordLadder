from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from .models import GameSettings
from django.contrib import messages
import requests
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


#====================================
# validation  functions
#====================================
def is_valid_word(word):
    # Merriam-Webster API endpoint
    api_key = "YOUR_MERRIAM_WEBSTER_API_KEY"
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # If the word is valid, the API returns a list of definitions
        if isinstance(data, list) and data:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error validating word: {e}")
        return False
    

def is_word_length_valid(new_word, start_word, end_word):
    return len(new_word) == len(start_word) == len(end_word)

def is_one_letter_changed(new_word, previous_word):
    if not previous_word:
        return True  # No previous word (first word in the ladder)
    
    # Normalize the words
    new_word = new_word.strip().lower()
    previous_word = previous_word.strip().lower()
    
    print(f"Comparing '{new_word}' with '{previous_word}'")  # Debugging
    
    if len(new_word) != len(previous_word):
        return False  # Words must be of the same length
    
    differences = sum(1 for a, b in zip(new_word, previous_word) if a != b)
    return differences == 1  

#====================================
# Add word functions
#====================================
def add_word(request, challenge_id):
    if request.method == "POST":
        # Fetch the challenge
        challenge = get_object_or_404(GameSettings, id=challenge_id)
        
        # Get the new word from the form
        new_word = request.POST.get("new_word").strip().lower()
        
        # Perform validation checks
        if not is_valid_word(new_word):
            messages.error(request, "The word is not a valid English word.")
        elif not is_word_length_valid(new_word, challenge.start_word, challenge.end_word):
            messages.error(request, "The word length does not match the start and end words.")
        else:
            # Get the previous word in the ladder
            previous_word = challenge.ladder[-1] if challenge.ladder else challenge.start_word
            if not is_one_letter_changed(new_word, previous_word):
                messages.error(request, "You can only change one letter at a time.")
            else:
                # Add the word to the ladder
                if not hasattr(challenge, 'ladder'):
                    challenge.ladder = []
                challenge.ladder.append(new_word)
                challenge.save()
                messages.success(request, f"Word '{new_word}' added to the ladder.")
        
        # Redirect back to the playground
        return redirect('playground', challenge_id=challenge.id)
    
    return redirect('home')
