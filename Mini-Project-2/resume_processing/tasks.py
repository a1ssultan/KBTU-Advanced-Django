from celery import shared_task
from django.conf import settings
from .models import Resume, ResumeAnalysis, Skill, Experience, Education
import PyPDF2
import docx
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy
import json

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

@shared_task
def process_resume(resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        resume.status = Resume.Status.PROCESSING
        resume.save()

        # Extract text from resume file
        text = extract_text_from_file(resume.file.path, resume.file_type)

        # Process text with spaCy
        doc = nlp(text)

        # Extract skills
        skills = extract_skills(doc)

        # Extract experience
        experience = extract_experience(doc)

        # Extract education
        education = extract_education(doc)

        # Extract keywords
        keywords = extract_keywords(text)

        # Create analysis
        analysis = ResumeAnalysis.objects.create(
            resume=resume,
            skills=skills,
            experience=experience,
            education=education,
            keywords=keywords
        )

        resume.status = Resume.Status.COMPLETED
        resume.save()

        return f"Successfully processed resume {resume_id}"

    except Exception as e:
        resume.status = Resume.Status.FAILED
        resume.save()
        raise e

def extract_text_from_file(file_path, file_type):
    if file_type == 'pdf':
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
    elif file_type == 'docx':
        doc = docx.Document(file_path)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    return text

def extract_skills(doc):
    skills = []
    for ent in doc.ents:
        if ent.label_ == 'SKILL':
            skills.append(ent.text)
    return skills

def extract_experience(doc):
    experience = []
    for sent in doc.sents:
        if any(word in sent.text.lower() for word in ['experience', 'worked', 'job', 'position']):
            experience.append(sent.text)
    return experience

def extract_education(doc):
    education = []
    for sent in doc.sents:
        if any(word in sent.text.lower() for word in ['education', 'degree', 'university', 'college']):
            education.append(sent.text)
    return education

def extract_keywords(text):
    # Tokenize text
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in tokens if word.isalnum() and word not in stop_words]
    
    return keywords 