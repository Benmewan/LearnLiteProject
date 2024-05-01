import os
import PyPDF2
from django.http import Http404
import openai
from django.shortcuts import render, redirect, get_object_or_404
from .models import TestDocument, GeneratedTest, Question
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dotenv import load_dotenv
import re

dotenv_path = os.path.join(os.path.dirname(__file__), 'key.env')
load_dotenv(dotenv_path=dotenv_path)
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("No API key loaded from environment variables")

@login_required
def add_test(request):
    print("Form submitted, method:", request.method)  
    if request.method == 'POST' and request.FILES.get('document'):
        doc_file = request.FILES['document']
        new_doc = TestDocument(uploaded_by=request.user, file=doc_file)
        new_doc.save()

        text = extract_text_from_pdf(doc_file)
        if text.strip():
            try:
                generate_test(new_doc, text)
                messages.success(request, "Test generated successfully.")
                return redirect('quizzes:all_tests')
            except Exception as e:
                messages.error(request, f"Test generation failed. Error: {str(e)}")
                print("Error during test generation:", e)
        else:
            messages.error(request, "No text could be extracted from the uploaded document.")
        return render(request, 'quizzes/upload_document.html')
    return render(request, 'quizzes/upload_document.html')

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_test(document, text):
    prompt = f"Create a test with 10 questions based on the following content, each with four options (A, B, C, D) and mark the correct answer clearly after each question in the format 'Correct Answer: X)':\n\n{text[:5000]}"
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=2000
        )
        print("API Response:", response)  

        if 'text' in response['choices'][0]:
            content = response['choices'][0]['text'].strip()
        elif 'message' in response['choices'][0] and 'content' in response['choices'][0]['message']:
            content = response['choices'][0]['message']['content'].strip()
        else:
            raise ValueError("Expected 'text' or 'message' with 'content' in the response is missing")
        
        questions_data = parse_questions_from_content(content)
        process_generated_test(questions_data, document)
    except Exception as e:
        error_msg = f"Failed to generate test with AI model: {str(e)}"
        print(error_msg)
        raise Exception(error_msg)


def process_generated_test(questions_data, document):
    # Check if there is any questions data to process
    if not questions_data:
        print("No questions data to process.")
        return
    # Create a new GeneratedTest instance associated with the document
    new_test = GeneratedTest(document=document, user=document.uploaded_by)
    new_test.save()
    # Iterate over each question data and create Question instances
    for question_data in questions_data:
        Question.objects.create(
            test=new_test,
            question_text=question_data['text'],
            choice_a=question_data['choices'][0],
            choice_b=question_data['choices'][1],
            choice_c=question_data['choices'][2],
            choice_d=question_data['choices'][3],
            correct_answer=question_data['correct_answer']  # Now storing the actual correct answer
        )

    print(f"Total questions saved: {new_test.questions.count()}")



def parse_questions_from_content(content):
    # Initialize an empty list to store parsed questions
    questions = []
    # Define the regex pattern to match question, choices, and correct answer
    pattern = r'\d+\.\s(.*?)(A\)\s.*?B\)\s.*?C\)\s.*?D\)\s.*?)\nCorrect Answer: ([ABCD])\)'
    # Find all matches of the pattern in the content
    matches = re.finditer(pattern, content, re.DOTALL)
    # Iterate over each match
    for match in matches:
        # Extract question text, choices, and correct answer from the match
        question_text = match.group(1).strip()
        choices_text = match.group(2).split('\n')
        correct_answer = match.group(3).lower()  # 'a', 'b', 'c', 'd'

        choices = [choice[3:].strip() for choice in choices_text]  # strip choice labels like 'A) '
        questions.append({
            'text': question_text,
            'choices': choices,
            'correct_answer': correct_answer
        })

    print(f"Parsed {len(questions)} questions")
    return questions


# Example API content
content = """
1. What are addition and subtraction called when working with numbers?\nA. Arithmetical divisions\nB. Arithmetical operations\nC. Arithmetical multiplications\nD. Geometry\n\nCorrect Answer: B. Arithmetical operations\n
2. Which operations are considered inverse operations?\nA. Addition and Division\nB. Subtraction and Multiplication\nC. Addition and Subtraction\nD. Multiplication and Division\n\nCorrect Answer: C. Addition and Subtraction\n
"""

# Assuming the content from the API is similar to the string defined above
questions = parse_questions_from_content(content)
print(questions)


@login_required
def view_generated_test(request, test_id):
    try:
        test = get_object_or_404(GeneratedTest, id=test_id)
    except Http404:
        return render(request, "main/not_exist.html")
    
    questions = test.questions.all()
    for question in questions:
        print("Q:", question.question_text)
        print("Choices:", question.choice_a, question.choice_b, question.choice_c, question.choice_d)
    
    return render(request, 'quizzes/generated_test.html', {'test': test, 'questions': questions})

    
@login_required
def submit_test(request, test_id):
    if request.method == 'POST':
        test = get_object_or_404(GeneratedTest, id=test_id)
        questions = test.questions.all()
        results = []
        total_score = 0

        for question in questions:
            user_answer = request.POST.get(f'answer_{question.id}')
            correct = user_answer == question.correct_answer
            if correct:
                total_score += 1

            results.append({
                'question_text': question.question_text,
                'user_answer': user_answer,
                'correct_answer': question.correct_answer,
                'is_correct': correct
            })

        score_percentage = (total_score / questions.count()) * 100 if questions.count() > 0 else 0
        return render(request, 'quizzes/test_result.html', {
            'score': total_score, 
            'percentage': score_percentage, 
            'total_questions': questions.count(),
            'results': results
        })

    return redirect('quizzes:all_tests')  

@login_required
def test_result(request, test_id):
    score = request.session.get('score', 0)
    total_questions = request.session.get('total_questions', 0)
    return render(request, 'quizzes/test_result.html', {'score': score, 'total_questions': total_questions})

@login_required
def save_test(request, test_id):
    return redirect('quizzes:all_tests')

@login_required
def discard_test(request, test_id):
    test = get_object_or_404(GeneratedTest, id=test_id)
    test.delete()
    return redirect('quizzes:all_tests')

@login_required
def all_tests(request):
    tests = GeneratedTest.objects.filter(user=request.user)
    return render(request, 'quizzes/all_tests.html', {'tests': tests})

@login_required
def all_tests(request):
    order = request.GET.get('order', 'newest')  # Get the 'order' parameter or default to 'newest'
    tests = GeneratedTest.objects.filter(user=request.user)
    
    if order == 'newest':
        tests = tests.order_by('-document__upload_date')  # Order by upload_date descending
    elif order == 'oldest':
        tests = tests.order_by('document__upload_date')  # Order by upload_date ascending
    
    return render(request, 'quizzes/all_tests.html', {'tests': tests, 'order': order})