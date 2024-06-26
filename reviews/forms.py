from django import forms

from reviews.models import Review


class CommentForm(forms.Form):
    text = forms.CharField(max_length=300, min_length=10)
    mark = forms.CharField(max_length=2, widget=forms.HiddenInput)
