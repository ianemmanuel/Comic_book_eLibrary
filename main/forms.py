from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import ComicReview
from demo_register import settings

# Review Add Form
class ReviewAdd(forms.ModelForm):
	class Meta:
		model=ComicReview
		fields=('review_text','review_rating')