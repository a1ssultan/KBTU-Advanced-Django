from celery import shared_task
from .models import Resume, ResumeAnalysis, ResumeFeedback
import PyPDF2
import docx
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

@shared_task
def analyze_resume(resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        text = extract_text_from_file(resume.file.path)
        
        # Initialize NLP
        nlp = spacy.load('en_core_web_sm')
        nltk.download('punkt')
        nltk.download('stopwords')
        
        # Extract information
        doc = nlp(text)
        skills = extract_skills(doc)
        experience = extract_experience(doc)
        education = extract_education(doc)
        
        # Calculate score
        score = calculate_score(skills, experience, education)
        
        # Create analysis
        analysis = ResumeAnalysis.objects.create(
            resume=resume,
            skills=skills,
            experience=experience,
            education=education,
            overall_score=score
        )
        
        # Generate feedback
        generate_feedback(resume, skills, experience, education)
        
        return True
    except Exception as e:
        print(f"Error analyzing resume: {str(e)}")
        return False

def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return text

def extract_skills(doc):
    skills = []
    for ent in doc.ents:
        if ent.label_ == 'SKILL':
            skills.append(ent.text)
    return skills

def extract_experience(doc):
    experience = []
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            experience.append(ent.text)
    return experience

def extract_education(doc):
    education = []
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            education.append(ent.text)
    return education

def calculate_score(skills, experience, education):
    score = len(skills) * 0.4 + len(experience) * 0.4 + len(education) * 0.2
    return min(score, 100)

def generate_feedback(resume, skills, experience, education):
    if len(skills) < 5:
        ResumeFeedback.objects.create(
            resume=resume,
            feedback_type='skill_gap',
            message='Your resume has fewer skills than average. Consider adding more relevant skills.',
            severity='medium'
        )
    
    if len(experience) < 2:
        ResumeFeedback.objects.create(
            resume=resume,
            feedback_type='formatting',
            message='Your experience section could be more detailed. Add specific achievements and responsibilities.',
            severity='high'
        )
    
    if len(education) < 1:
        ResumeFeedback.objects.create(
            resume=resume,
            feedback_type='ats',
            message='Your education section is missing. Add your educational background.',
            severity='high'
        ) 