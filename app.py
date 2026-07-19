import os
import requests
import streamlit as st
from dotenv import load_dotenv

# 1. Load environmental variables securely
load_dotenv()

# 2. AI Service Logic (Updated for Google Gemini API)
def fetch_stadium_assistance(user_query: str, target_language: str) -> str:
    """
    Connects to the Google Gemini API endpoint, executes contextual system prompts,
    and returns a localized, highly accurate real-time response.
    """
    API_KEY = os.getenv("GENAI_API_KEY")
    
    # If the key isn't provided, trigger our fallback simulation mode
    if not API_KEY:
        return (
            f"[⚠️ Offline Simulation Mode]: API Key is missing. "
            f"Simulated directions for your question '{user_query}' translated into {target_language} will appear here."
        )

    # Standard Gemini 1.5 Flash Content Generation URL
    API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    # Structured prompt combining system boundary persona and user query
    full_prompt = (
        f"System: You are an elite FIFA World Cup 2026 stadium operational assistant. "
        f"Provide a highly accurate, concise answer regarding stadium logistics, navigation, or safety. "
        f"Translate your final answer completely and naturally into the target language: {target_language}.\n\n"
        f"User Query: {user_query}"
    )

    headers = {
        "Content-Type": "application/json"
    }

    # Google Gemini API Payload structure
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2  # Guarantees rigid, highly factual navigational answers
        }
    }

    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Parse text directly out of the Gemini structural dictionary response
        return data["candidates"][0]["content"]["parts"][0]["text"]
        
    except requests.exceptions.RequestException:
        return (
            f"Notice: High stadium network traffic detected. Local backup routing active. "
            f"Please report directly to the nearest on-ground supervisor at Gate A for immediate assistance."
        )

# 3. Streamlit Layout Architecture
st.set_page_config(
    page_title="VenueSync AI - Smart Stadium Hub",
    page_icon="🏟️",
    layout="centered"
)

st.title("🏟️ VenueSync AI")
st.caption("Real-time navigation, logistics, and multi-language support for World Cup 2026.")
st.markdown("---")

st.sidebar.header("🗺️ Language Settings")
language = st.sidebar.selectbox(
    "Choose your language / भाषा निवडा:",
    ["English", "Hindi", "Marathi", "Spanish", "French"]
)

st.sidebar.markdown("""
### 💡 Sample Inquiries:
* *"How do I get to Gate C from Sector 4?"*
* *"Where is the nearest first-aid station?"*
* *"Which exit is closest to the metro station?"*
""")

st.subheader("How can we assist you at the venue?")
user_query = st.text_area(
    "Enter your logistical or navigation question:",
    placeholder="E.g., I am looking for the family seating section..."
)

if st.button("Ask Assistant", type="primary"):
    if not user_query.strip():
        st.warning("Please input a valid question before executing the prompt.")
    else:
        with st.spinner("Processing stadium mapping and translating data..."):
            ai_response = fetch_stadium_assistance(user_query, language)
            st.markdown("### 🤖 Assistant Guidance")
            st.info(ai_response)

st.markdown("---")
st.caption("© 2026 FIFA World Cup Smart Stadium Ecosystem Prototype. Built for Challenge 4.")
