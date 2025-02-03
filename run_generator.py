from models.generators import generate_pitch_deck

if __name__ == "__main__":
    prompt = "AI-powered coffee mug"  # title
    slides = generate_pitch_deck(prompt)
    print(f"\nGenerated {len(slides)} slides!")
