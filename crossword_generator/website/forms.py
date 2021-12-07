from django import forms

class SolutionForm(forms.Form):
    letters = forms.CharField(required=False)