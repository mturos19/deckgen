# 🚀 AI Pitch Deck Generator
Automate VC-style pitch decks using generative AI. Think "Uber for X" meets Stable Diffusion.


# 📖 Overview
An AI-powered tool that generates startup pitch decks (PDF) including:

* AI-generated startup ideas (GPT-4)

* Mockup visuals (Stable Diffusion XL)

* Market sizing slides (synthetic data)

* Buzzword compliance scoring (RoBERTa)

Use Case: Accelerate ideation for founders, VCs, and innovation workshops.

# ✨ Features
* AI-Generated Content: Titles, problem statements, TAM/SAM/SOM slides.

* Dynamic Visuals: Unique app/UIs generated for each concept.

* Fake Metrics Engine: "10X growth" charts with synthetic time-series data.

* One-Click PDF Export: Professional slide decks in 2 clicks.

* BuzzScore™: Quantify buzzword density using NLP.

# ⚙️ Installation
Requirements: Python 3.10+, 8GB RAM (Stable Diffusion runs locally).


* git clone https://github.com/mturos19/deckgen
* cd deckgen
* pip install -r requirements.txt
* Get an OpenAI API key

* Get a HuggingFace token (for Stable Diffusion)

* Create .env file:
OPENAI_API_KEY=your_key_here
HF_TOKEN=your_hf_token_here

# 🎮 Usage
Run the app:

streamlit run app/main.py

Generate a deck:

* Input a trend (e.g., "vertical farming with NFTs")

* Adjust slides using the sidebar

* Export to PDF

# Analyze buzzwords:

* Click "Calculate BuzzScore™" to see how Silicon Valley-ready your deck is.

# 🛠️ Customization

* Modify prompts: Edit prompts/idea_prompts.json to steer GPT-4’s creativity.

* Change themes: Update CSS in app/styles.css.

* Add new models: Clone the BaseGenerator class in models/generators.py.
