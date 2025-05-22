import streamlit as st
import google.generativeai as genai
import os

# 🔹 Set Streamlit Page Config
st.set_page_config(page_title="📝 AI-Based Plagiarism Checker", page_icon="📝", layout="centered")

# 🔹 Secure API Key Handling
API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyBBTNFznyQOKaD56pYb-dXxwbp8bGYOXAI"  # Replace with your actual API key
if API_KEY:
    genai.configure(api_key=API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("⚠️ Gemini AI API key is missing! Plagiarism detection may not work.")

# 🔹 Supported Languages for Translation
languages = {
    "English": "English",
    "Urdu": "اردو",
    "Sindhi": "سنڌي",
    "Punjabi (Shahmukhi)": "پنجابی",
    "Pashto": "پښتو",
    "Balochi": "بلوچی",
    "Gujarati": "ગુજરાતી",
    "Hindko": "ہندکو",
    "Wakhi": "وخی",
}

# 🔹 Function to Translate Text Using Gemini AI
def translate_text(text, target_language):
    if not API_KEY:
        return text  # If no API key, return the original text
    try:
        prompt = f"Translate the following text to {target_language}:\n\n{text}"
        response = gemini_model.generate_content(prompt)
        if response and hasattr(response, "text") and response.text.strip():
            return response.text.strip()
        else:
            return text
    except Exception as e:
        st.error(f"⚠️ Translation Error: {str(e)}")
        return text

# 🔹 AI-Based Plagiarism Detection
st.title("📝 AI-Based Plagiarism Checker")
st.write("Paste the text below to check for plagiarism.")

# User Input for Text
input_text = st.text_area("Paste your text here:", placeholder="Enter or paste your text...")

# Language Selection Dropdown for Translation
selected_language = st.selectbox("🌍 Select language for result:", options=list(languages.keys()))

# Check Plagiarism Button
if st.button("Check Plagiarism"):
    if not input_text.strip():
        st.error("Please enter some text to check!")
    else:
        st.info("Analyzing text for plagiarism... Please wait.")
        prompt = (f"Analyze the following text for plagiarism by checking its similarity with common sources "
                  f"such as online articles, books, and research papers. Provide a detailed plagiarism percentage "
                  f"and highlight possible sources:\n\n{input_text}")
        
        try:
            response = gemini_model.generate_content(prompt)
            if response and hasattr(response, "text") and response.text.strip():
                plagiarism_report = response.text.strip()
                # Translate if the selected language is not English
                if selected_language != "English":
                    plagiarism_report = translate_text(plagiarism_report, languages[selected_language])
                st.success("Plagiarism Check Completed!")
                st.write(plagiarism_report)
            else:
                st.error("⚠️ No response received. Please try again.")
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")

# 🔹 Footer
st.markdown("---")
st.markdown("🚀 **Developed by Muhammad Mudasir** | AI-Based Plagiarism Checker")
