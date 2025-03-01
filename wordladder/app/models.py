from django.db import models

class GameSettings(models.Model):
    GAME_MODES = [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    CHALLENGE_TYPES = [('predefined', 'Predefined'), ('custom', 'Custom')]
    AI_HINTS = [('A*', 'A*'), ('UCS', 'UCS'), ('BFS', 'BFS')]

    game_mode = models.CharField(max_length=20, choices=GAME_MODES)
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES)
    start_word = models.CharField(max_length=100)
    end_word = models.CharField(max_length=100)
    ai_hint = models.CharField(max_length=20, choices=AI_HINTS, blank=True, null=True)
    current_word = models.CharField(max_length=100, blank=True)
    ladder = models.JSONField(default=list)  

    easy_moves = models.IntegerField(default=5, editable=False)
    medium_moves = models.IntegerField(default=10, editable=False)
    hard_moves = models.IntegerField(default=15, editable=False)
    current_moves = models.IntegerField(default=0)

    victory = models.BooleanField(default=False)  # ✅ Added victory field

    def save(self, *args, **kwargs):
        """Ensure current_word is initialized to start_word and check for victory."""
        if not self.current_word:
            self.current_word = self.start_word

        # ✅ Mark victory when current_word == end_word
        if self.current_word == self.end_word:
            self.victory = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Game: {self.start_word} → {self.end_word} | Mode: {self.game_mode} | Moves: {self.current_moves} | Victory: {self.victory}"
