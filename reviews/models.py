# reviews/models.py
from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=150)
    genre = models.CharField(max_length=120)             # e.g. "Action, Sci-Fi"
    rating = models.FloatField(default=0)                # IMDb rating (0 if unknown)
    description = models.TextField(blank=True)
    poster_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    stars = models.PositiveSmallIntegerField(default=0)   # 0–10 or 0–5; we’ll use 0–10
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.movie.title}"



