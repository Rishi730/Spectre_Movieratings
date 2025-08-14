# reviews/forms.py
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["stars", "text"]
        widgets = {
            "stars": forms.NumberInput(attrs={"min": 0, "max": 10}),
            "text": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "stars": "Give a rating from 0 to 10."
        }
