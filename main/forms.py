from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import ComicReview, Comic
from demo_register import settings

# Review Add Form
class ReviewAdd(forms.ModelForm):
	class Meta:
		model=ComicReview
		fields=('review_text','review_rating')


class ComicForm(forms.ModelForm):
	class Meta:
		model = Comic
		fields = ('title', 'detail', 'image', 'comicBook', 'price', 'category', 'publisher', 'vendor')

		widgets = {
			'title' : forms.TextInput(attrs={'class':'form-control'}),
			'detail' : forms.Textarea(attrs={'class':'form-control'}),
			# 'image' : forms.TextInput(attrs={'class':'form-control'}),
			# 'comicBook' : forms.TextInput(attrs={'class':'form-control'}),
			'price' : forms.NumberInput(attrs={'class':'form-control'}),
			'category' : forms.Select(attrs={'class':'form-control'}),
			'publisher' : forms.Select(attrs={'class':'form-control'}),
			'vendor' : forms.Select(attrs={'class':'form-control'}),
		
		}