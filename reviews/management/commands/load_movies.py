# reviews/management/commands/load_movies.py
import os
import time
import requests
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Movie

OMDB_URL = "http://www.omdbapi.com/"

HOLLYWOOD_TITLES = [
    "Inception", "Interstellar", "The Dark Knight", "The Matrix",
    "Titanic", "Avatar", "Gladiator", "Fight Club", "Pulp Fiction",
    "The Shawshank Redemption", "Forrest Gump", "The Godfather"
]

class Command(BaseCommand):
    help = "Loads a set of Hollywood movies from OMDb into the database."

    def add_arguments(self, parser):
        parser.add_argument("--titles", nargs="*", help="Custom titles (optional).")

    def handle(self, *args, **options):
        api_key = os.environ.get("OMDB_API_KEY")
        if not api_key:
            raise CommandError("OMDB_API_KEY is not set in environment.")

        titles = options["titles"] or HOLLYWOOD_TITLES
        created_count = 0

        for title in titles:
            params = {"apikey": api_key, "t": title}
            r = requests.get(OMDB_URL, params=params, timeout=20)
            data = r.json()

            if data.get("Response") != "True":
                self.stdout.write(self.style.WARNING(f"Skipped: {title} — {data.get('Error')}"))
                continue

            imdb_rating = data.get("imdbRating")
            try:
                rating = float(imdb_rating) if imdb_rating and imdb_rating != "N/A" else 0.0
            except ValueError:
                rating = 0.0

            obj, created = Movie.objects.get_or_create(
                title=data.get("Title", title),
                defaults={
                    "genre": data.get("Genre", ""),
                    "rating": rating,
                    "description": data.get("Plot", ""),
                    "poster_url": data.get("Poster", ""),
                },
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Added: {obj.title}"))
            else:
                self.stdout.write(f"Exists: {obj.title}")

            time.sleep(0.2)  # be polite

        self.stdout.write(self.style.SUCCESS(f"Done. Created {created_count} movies."))
