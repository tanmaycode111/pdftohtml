

# Create your views here.
# editor/views.py
import os
import pdfplumber
from weasyprint import HTML
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from bs4 import BeautifulSoup

def upload_pdf(request):
    if request.method == "POST":
        uploaded_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # Convert PDF to HTML
        html_content = pdf_to_html(fs.path(filename))

        context = {
            'html_content': html_content,
            'file_url': file_url
        }
        return render(request, 'editor/edit_pdf.html', context)

    return render(request, 'editor/upload.html')

def pdf_to_html(pdf_path):
    # Extract text and images from the PDF
    with pdfplumber.open(pdf_path) as pdf:
        html_content = "<html><body>"
        for page in pdf.pages:
            text = page.extract_text()
            # You can also extract images, styles, etc.
            html_content += f"<div>{text}</div>"
        html_content += "</body></html>"

    return html_content

def save_edited_html(request):
    if request.method == "POST":
        html_content = request.POST['html_content']
        
        # Save the edited HTML back to PDF
        pdf_file = html_to_pdf(html_content)
        
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="edited_pdf.pdf"'
        return response

def html_to_pdf(html_content):
    # Convert the edited HTML to a PDF
    pdf_file = HTML(string=html_content).write_pdf()
    return pdf_file
