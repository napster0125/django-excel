from django import forms

class SubmissionForm(forms.Form):
	cfile=forms.FileField()
