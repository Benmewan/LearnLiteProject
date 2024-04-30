import os
from django.shortcuts import render, redirect,get_object_or_404
from .models import Document, Summary
import PyPDF2
import openai
from dotenv import load_dotenv
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
import markdown


dotenv_path = os.path.join(os.path.dirname(__file__), 'key.env')
load_dotenv(dotenv_path=dotenv_path)

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("No API key loaded from environment variables")


@login_required
def add_summary(request):
    if request.method == 'POST' and request.FILES.get('document'):
        doc_file = request.FILES['document']
        new_doc = Document(uploaded_by=request.user, file=doc_file)
        new_doc.save()

        text = extract_text_from_pdf(doc_file)
        if text.strip():
            prompt = "Summarize the following document in detail: " + text[:5000]
            try:
                content = get_completion(prompt)
                new_summary = Summary(document=new_doc, user=request.user, content=content, complexity_level=request.POST.get('complexity', 'main_points'), status='completed')
                new_summary.save()
                messages.success(request, "Summary generated successfully.")
                return redirect('summary:display_summary', summary_id=new_summary.id)
            except Exception as e:
                messages.error(request, f"Summary generation failed. Error: {str(e)}")
                return render(request, 'summary/add_summary.html')
        else:
            messages.error(request, "No text could be extracted from the uploaded document.")
            return render(request, 'summary/add_summary.html')
    return render(request, 'summary/add_summary.html')


def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_completion(prompt):
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    structured_prompt = f"Summarize the following content clearly with bullet points or numbered sections: {prompt}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant, please summarize the text in a structured format."},
                {"role": "user", "content": structured_prompt}
            ],
        )
        content = response['choices'][0]['message']['content'].strip()

        # Convert Markdown to HTML
        html_content = markdown.markdown(content)
        return html_content
    except Exception as e:
        raise Exception(f"Failed to generate completion with chat model: {str(e)}")

def display_summary(request, summary_id):
    try:
        summary = get_object_or_404(Summary, id=summary_id)
        # Convert Markdown content to HTML
        summary.content = markdown.markdown(summary.content)
        return render(request, 'summary/display_summary.html', {'summary': summary})
    except Http404:
        return render(request, "main/not_exist.html")

@login_required
def list_summaries(request):
    order = request.GET.get('order', 'newest')  # Default to 'newest' if not specified

    if order == 'oldest':
        summaries = Summary.objects.filter(user=request.user).order_by('document__upload_date')
    else:  # Defaults to newest
        summaries = Summary.objects.filter(user=request.user).order_by('-document__upload_date')

    return render(request, 'summary/list_summaries.html', {'summaries': summaries, 'order': order})

def save_summary(request, summary_id):
    return redirect('summary:list_summaries')

def discard_summary(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id)
    summary.delete()  
    return redirect('summary:list_summaries')  
