import re
from app.services.gemini_service import generate_solution
from app.services.geocode_service import get_location

#Categorization based on keywords
def categorize_problem(problem: str):
    text = problem.lower()
    if "road" in text or "traffic" in text:
        return "Infrastructure"
    elif "water" in text or "electricity" in text:
        return "Utilities"
    elif "garbage" in text or "sanitation" in text:
        return "Sanitation"
    elif any(word in text for word in ["hospital", "doctor", "medicine", "ambulance", "health"]):
        return "Medical"
    else:
        return "Other"
    

#Priority assignment based on keywords
def assign_priority(problem: str):
    text = problem.lower()
    if any(word in text for word in ["accident", "fire", "collapse", "emergency", "ambulance", "health"]):
        return "High"
    elif any(word in text for word in ["pothole", "flood", "supply issue", "power cut"]):
        return "Medium"
    else:
        return "Low"
    
#Extract location using geocoding service
def extract_location(text: str):
    pattern = r'\b(?:in|at|near|around)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b'
    match = re.search(pattern, text)
    return match.group(1) if match else "Unknown Location"

#Main Processing Pipeline
def process_grievance(problem_text: str):
    category = categorize_problem(problem_text)
    priority = assign_priority(problem_text)
    region = extract_location(problem_text)
    location = get_location(region)
    solution = generate_solution(problem_text)

    return {
        "description": problem_text,
        "category": category,
        "priority": priority,
        "region": region,
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
        "solution": solution
    }