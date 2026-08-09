from fastapi import APIRouter, HTTPException
from app.services.gemini_service import generate_solution

router = APIRouter(prefix="/ai", tags=["AI Processing"])

@router.post("/analyze")
def analyze_grievance(input_text: dict):
    """
    Uses Gemini/OpenAI to detect grievance category, priority, and region
    from natural language.
    """
    description = input_text.get("description")
    if not description:
        raise HTTPException(status_code=400, detail="Missing grievance description")

    prompt = f"""
    You are an AI assistant that classifies citizen grievances into structured fields.
    Given the following user complaint: "{description}", respond in strict JSON only:
    {{
      "category": "<category like Water, Electricity, Roads, Sanitation>",
      "priority": "<High | Medium | Low>",
      "region": "<Extract or infer region name if present, else 'Unknown'>"
    }}
    """

    response = generate_solution(prompt)
    return response
