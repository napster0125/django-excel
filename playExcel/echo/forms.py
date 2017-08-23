from django import forms

class ScriptForm(forms.Form):
    field = forms.CharField()