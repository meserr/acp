from django import forms

class ReadFileForm(forms.Form):
    file = forms.FileField(
        label="Select Fasta File",
    )