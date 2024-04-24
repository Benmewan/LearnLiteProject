import os
from django.shortcuts import render, redirect,get_object_or_404
from .models import Document, Summary
import PyPDF2
import openai
from dotenv import load_dotenv
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator



dotenv_path = os.path.join(os.path.dirname(__file__), 'key.env')
load_dotenv(dotenv_path=dotenv_path)

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("No API key loaded from environment variables")


def add_summary(request):
    if request.method == 'POST' and request.FILES.get('document'):
        doc_file = request.FILES['document']
        new_doc = Document(uploaded_by=request.user, file=doc_file)
        new_doc.save()

        # Extract text from PDF
        text = extract_text_from_pdf(doc_file)

        # Only attempt to generate a summary if there's text extracted
        if text.strip():
            prompt = f"Summarize the document content: {text[:2000]}"
            try:
                content = get_completion(prompt)
                new_summary = Summary(document=new_doc, content=content)
                new_summary.save()
                messages.success(request, "Summary added successfully.")
                return redirect('summary:display_summary', summary_id=new_summary.id)  
            except Exception as e:
                print("API generation failed:", e)
                messages.error(request, f"Summary generation failed. Error: {str(e)}")
        else:
            messages.error(request, "No text could be extracted from the uploaded document.")
    return render(request, 'summary/add_summary.html')


def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_completion(prompt):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key is not available")
    
    openai.api_key = api_key  # Ensure the API key is set

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                      {"role": "user", "content": prompt}],
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Failed to generate completion with chat model: {str(e)}")
        raise

def display_summary(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id)
    return render(request, 'summary/display_summary.html', {'summary': summary})


def view_summary(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id, user=request.user)
    return render(request, 'summary/detail.html', {'summary': summary})


def list_summaries(request):
    summaries = Summary.objects.all()  
    return render(request, 'summary/list_summaries.html', {'summaries': summaries})

