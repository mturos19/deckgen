import pytest
from models.generators import generate_pitch_deck
import os
from dotenv import load_dotenv
import json

load_dotenv()

def test_generate_pitch_deck():
    api_key = os.getenv("api_key")
    if not api_key:
        pytest.skip("api_key not set in environment variables")
    
    outputs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    
    try:
        slides = generate_pitch_deck(
            prompt="Create a pitch deck for: Uber but for pet rocks",
            api_key=api_key
        )
        
        print("\nGenerated Pitch Deck:")
        for i, slide in enumerate(slides, 1):
            print(f"\nSlide {i}:")
            print(f"Title: {slide['title']}")
            print(f"Content: {slide['content']}")
        
        output_files = [f for f in os.listdir(outputs_dir) if f.endswith('.json')]
        assert len(output_files) > 0, "No output file was created"
        
        latest_file = max(output_files, 
                         key=lambda x: os.path.getctime(os.path.join(outputs_dir, x)))
        
        with open(os.path.join(outputs_dir, latest_file)) as f:
            saved_data = json.load(f)
            assert "timestamp" in saved_data
            assert "prompt" in saved_data
            assert "slides" in saved_data
            assert saved_data["slides"] == slides
        
        assert isinstance(slides, list), "Output should be a list"
        assert len(slides) == 5, "Should have exactly 5 slides"
        
        for i, slide in enumerate(slides):
            assert isinstance(slide, dict), f"Slide {i} should be a dictionary"
            assert "title" in slide, f"Slide {i} missing title"
            assert "content" in slide, f"Slide {i} missing content"
            assert isinstance(slide["title"], str), f"Slide {i} title should be string"
            assert isinstance(slide["content"], str), f"Slide {i} content should be string"
            
    except Exception as e:
        pytest.fail(f"Test failed with error: {str(e)}")
