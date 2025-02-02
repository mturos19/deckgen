import json
import os
import time
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_key")
if not api_key:
    raise ValueError("API key not found in environment variables")

def save_to_json(data: dict) -> str:
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(current_dir, '..', 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        
        filename = os.path.join(output_dir, f"pitch_deck_{data['timestamp']}.json")
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        return filename
    except Exception as e:
        print(f"Error saving JSON: {e}")
        raise

def generate_pitch_deck(prompt: str, api_key: str = None) -> list:
    print("Starting pitch deck generation...")

    if api_key is None:
        load_dotenv()
        api_key = os.getenv("api_key")
        if not api_key:
            raise ValueError("API key not found in environment variables")
            
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Pitch Deck Generator",
        }
    )
    
    system_message = '''You are a parody startup pitch deck generator. Generate a JSON object with the following structure:
    {
        "slides": [
            {"title": "Slide Title", "content": "Slide Content"},
            // ... 5 slides total
        ]
    }
    Include:
    - Exactly 5 slides
    - Satirical tech buzzwords
    - Comically overambitious claims'''
    
    max_attempts = 5
    attempt = 0
    response = None
    
    while attempt < max_attempts:
        try:
            print(f"Making API request... (attempt {attempt+1})")
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1:free",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Generate a pitch deck for: {prompt}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
    
            if (response.choices and 
                response.choices[0].message and 
                response.choices[0].message.content and 
                response.choices[0].message.content.strip()):
                break
        except Exception as e:
            print(f"Error during API request: {str(e)}")
    
        err = getattr(response, "error", None)
        if err and err.get("code") == 429:
            print("Rate limit exceeded. Waiting 5 seconds before retrying...")
        else:
            print("API response did not include valid content. Retrying in 5 seconds...")
        time.sleep(5)
        attempt += 1
    
    if attempt == max_attempts:
        raise ValueError("Exceeded maximum API call attempts due to rate limiting or invalid API response.")
    
    raw_content = response.choices[0].message.content
    print(f"Raw API response: {raw_content}")
    
    cleaned_content = raw_content.strip()
    if cleaned_content.startswith("```json"):
        cleaned_content = cleaned_content[7:]
    if cleaned_content.endswith("```"):
        cleaned_content = cleaned_content[:-3]
    cleaned_content = cleaned_content.strip()
    
    def escape_control_chars(s: str) -> str:
        out = []
        in_string = False
        escape = False
        for ch in s:
            if in_string:
                if escape:
                    out.append(ch)
                    escape = False
                else:
                    if ch == '\\':
                        out.append(ch)
                        escape = True
                    elif ch == '"':
                        out.append(ch)
                        in_string = False
                    elif ch == "\n":
                        out.append("\\n")
                    elif ch == "\r":
                        out.append("\\r")
                    else:
                        out.append(ch)
            else:
                if ch == '"':
                    out.append(ch)
                    in_string = True
                else:
                    out.append(ch)
        return "".join(out)
    
    fixed_content = escape_control_chars(cleaned_content)
    
    try:
        response_content = json.loads(fixed_content)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error. Fixed content: {fixed_content}")
        raise ValueError(f"Invalid JSON response after escaping control characters: {str(e)}")
    
    if "slides" not in response_content:
        raise ValueError(f"Response missing 'slides' key. Got: {response_content}")
    
    slides = response_content["slides"]
    if len(slides) != 5:
        raise ValueError(f"Expected 5 slides, got {len(slides)}")
    
    for i, slide in enumerate(slides):
        if not isinstance(slide, dict) or "title" not in slide or "content" not in slide:
            raise ValueError(f"Invalid slide structure at slide {i+1}")
    
    output_data = {
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "prompt": prompt,
        "slides": slides
    }
    filename = save_to_json(output_data)
    print(f"Saved pitch deck to: {filename}")
    
    return slides
