# editor/forms.py
from django import forms

class UploadPDFForm(forms.Form):
    pdf_file = forms.FileField()
