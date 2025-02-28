from django.db import models

class GameSettings(models.Model):
    GAME_MODES = [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    CHALLENGE_TYPES = [('predefined', 'Predefined'), ('custom', 'Custom')]
    AI_HINTS = [('A*', 'A*'), ('UCS', 'UCS'), ('BFS', 'BFS')]

    game_mode = models.CharField(max_length=20, choices=GAME_MODES)
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES)
    start_word = models.CharField(max_length=100)
    end_word = models.CharField(max_length=100)
    ai_hint = models.CharField(max_length=20, choices=AI_HINTS)
    input_word = models.CharField(max_length=100)
    ladder = models.JSONField(default=list)
    def __str__(self):
        return f"Game settings: {self.start_word} to {self.end_word}"
