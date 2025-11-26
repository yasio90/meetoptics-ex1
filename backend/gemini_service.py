import os
from dotenv import load_dotenv
import google.generativeai as genai


# custom exception for this service
class GeminiServiceError(Exception):
    pass


# load environment variables
load_dotenv()

def get_summary_from_gemini(text: str) -> str:
    """
    Interacts with the Google Gemini API to summarize the given text.

    Args:
        text: The text to be summarized.

    Returns:
        The summarized text as a string.
        
    Raises:
        ValueError: If the API key is not found in the environment variables.
        Exception: For other issues during API interaction.
    """
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
        
    try:
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"Please provide a concise summary of the following text:\n\n---\n\n{text}"
        
        response = model.generate_content(prompt)
        
        # check if the response is non-empty
        if response.text:
            return response.text
        else:
            # probably should handle this more gracefully
            return "*Could not generate a summary for the provided text.*"

    except Exception as e:
        # logging of the exception would be useful
        print(f"An unexpected error occurred in the Gemini service: {e}")
        raise GeminiServiceError(f"Failed to communicate with the Gemini API: {e}")
