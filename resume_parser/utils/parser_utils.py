import pdfplumber
import re
import frappe


def extract_text_from_pdf(file_path):
    """Extract text safely from PDF"""
    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception:
        frappe.log_error(frappe.get_traceback(), "PDF Extraction Failed")

    return text.strip()


def extract_skills(text):
    """Improved keyword + regex-based skill extraction"""

    keywords = [
        "python", "java", "sql", "machine learning",
        "deep learning", "nlp", "pandas", "numpy",
        "tensorflow", "pytorch", "django", "flask"
    ]

    text_lower = text.lower()
    found_skills = set()

    for skill in keywords:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return list(found_skills)


def calculate_score(skills):
    """Weighted scoring system (better than flat scoring)"""

    weights = {
        "python": 25,
        "machine learning": 25,
        "deep learning": 20,
        "nlp": 20,
        "sql": 15,
        "java": 15,
        "pandas": 10,
        "numpy": 10,
        "tensorflow": 20,
        "pytorch": 20,
        "django": 10,
        "flask": 10
    }

    score = sum(weights.get(skill, 10) for skill in skills)

    return min(score, 100)


def parse_resume(file_path):
    """Main pipeline"""

    text = extract_text_from_pdf(file_path)

    if not text:
        return {
            "skills": "",
            "score": 0
        }

    skills = extract_skills(text)
    score = calculate_score(skills)

    return {
        "skills": ", ".join(sorted(skills)),
        "score": score
    }
