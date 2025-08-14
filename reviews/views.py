# reviews/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Movie, Review
from .forms import ReviewForm

def movie_list(request):
    """
    List all movies, with optional ?genre=Action filter and ?q=search.
    """
    qs = Movie.objects.all().order_by("title")

    genre = request.GET.get("genre")
    if genre:
        # genre is stored as a CSV string, so partial match works:
        qs = qs.filter(genre__icontains=genre)

    q = request.GET.get("q")
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

    # Build a small list of popular genres (from our data)
    genres = (
        Movie.objects.exclude(genre="")
        .values_list("genre", flat=True)
    )
    # Flatten CSV genres into a unique set
    genre_set = set()
    for g in genres:
        for piece in g.split(","):
            piece = piece.strip()
            if piece:
                genre_set.add(piece)

    return render(request, "reviews/movie_list.html", {
        "movies": qs,
        "genres": sorted(genre_set),
        "active_genre": genre or "",
        "q": q or "",
    })

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, "reviews/movie_detail.html", {"movie": movie})

@login_required
def add_review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect("movie_detail", pk=movie.pk)
    else:
        form = ReviewForm()
    return render(request, "reviews/review_form.html", {"form": form, "movie": movie})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("movie_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def logout_view(request):
    """Custom logout view that accepts GET requests"""
    auth_logout(request)
    return redirect('movie_list')

# Create your views here.
