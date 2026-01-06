import os
import re
from google import genai


client = genai.Client(
    #api_key=os.getenv("GEMINI_API_KEY")  
    api_key="AIzaSyDFRK-pZDbmeYJQyj3-JbQPedyYAjWmNLQ"
)

MODEL_NAME = "gemini-3-flash-preview"


def clean_llm_lines(lines, max_words=12):
    """
    Cleans and filters raw LLM output lines to remove meta responses,
    markdown artifacts, and overly verbose content.
    """
    cleaned = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        # Drop assistant / meta responses
        if any(bad in lower for bad in [
            "i cannot",
            "i do not have access",
            "it appears",
            "here is",
            "this file",
            "prompt",
            "as an ai",
            "```"
        ]):
            continue

        # Remove markdown artifacts
        line = re.sub(r"[#>*`]", "", line).strip()

    
        if len(line.split()) > max_words:
            continue

        cleaned.append(line)

    return cleaned


def generate_batch(prompt, n=20, temperature=0.7):
   
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        
    )

    if not hasattr(response, "text") or not response.text:
        return []

    raw_lines = [
        l.strip("-• ")
        for l in response.text.split("\n")
        if l.strip()
    ]

    cleaned = clean_llm_lines(raw_lines)

    return cleaned[:n]
