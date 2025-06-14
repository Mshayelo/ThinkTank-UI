# ThinkTank-UI – Streamlit Frontend for Document Chatbot 

ThinkTank-UI is the user-facing frontend of the ThinkTank AI system, built with Streamlit. Designed for internal sales teams, it enables users to chat with documents, extract insights, and explore business content dynamically.

# Highlights
Secure login using streamlit-authenticator

Drag-and-drop PDF upload

Built-in prompts for faster onboarding

Natural language chat powered by GPT-4o

Session-based chat history (non-persistent)

Tailored for Think Tank Software Solutions Sales Team

# Getting Started
Clone or download the repo:

git clone https://github.com/<your-org>/ThinkTank-UI.git
Or download as ZIP and extract.

# Set up your virtual environment:

cd ThinkTank-UI
python -m venv venv
source venv/bin/activate      # macOS/Linux  
venv\Scripts\activate         # Windows
pip install -r requirements.txt

# Set backend URL:
Open frontend.py and update:

BACKEND_URL = "http://localhost:5000"

# Add login credentials:
Ensure hashed_pw.pk1 is present in the root folder. If missing, generate using:
python generate_keys.py

# Run the app:

streamlit run frontend.py
Visit http://localhost:8501 to use the chatbot interface.

# Folder Overview
File	Description
frontend.py	Main Streamlit application
generate_keys.py	Helper script for generating login hash
hashed_pw.pk1	Encrypted login credentials
tt.png	UI branding/logo
README.md - Current file.

# Designed For
ThinkTank-UI was developed to empower Sales Professionals at Think Tank Software Solutions. It’s especially useful for:

New team members needing to quickly understand documents

Sales managers reviewing proposals or decks

Anyone needing intelligent, fast summaries without digging through full PDFs

# Why It Matters
ThinkTank AI bridges the gap between lengthy documentation and actionable insights. It reduces preparation time, enhances comprehension, and enables smarter client engagement — making it a true competitive edge for the sales team.


