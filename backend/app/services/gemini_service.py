import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_solution(grievance_text: str):
    """
    Generates a structured short-term and long-term solution using Gemini AI.
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash') # Or 'gemini-pro'
        
        # We enforce a specific structure in the prompt
        prompt = (
            f"Act as a government grievance redressal expert. "
            f"Analyze this citizen complaint: '{grievance_text}'.\n\n"
            f"Provide a structured response with exactly these two sections:\n"
            f"1. **Short-term Action:** (Immediate steps to resolve the specific issue within 24-48 hours)\n"
            f"2. **Long-term Solution:** (Systemic changes or infrastructure upgrades to prevent recurrence)\n\n"
            f"Keep the tone professional and empathetic."
        )
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Solution generation unavailable at the moment."