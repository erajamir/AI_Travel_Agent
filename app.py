import streamlit as st
import speech_recognition as sr
import openai
import pyttsx3

# 🔑 Add your ChatGPT API key here
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 🌍 Set page config
st.set_page_config(page_title="World Travel Guide", page_icon="🌍", layout="wide")

# 🌄 Background image + Custom CSS
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    color: black;
    font-family: 'Segoe UI', sans-serif;
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

h1, h2, h3, p, .stMarkdown {
    color: black !important;
    text-shadow: none;
}

.center {
    display: flex;
    justify-content: center;
    align-items: center;
}

.stButton>button {
    background-color: rgba(255, 255, 255, 0.7);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    padding: 12px 30px;
    font-size: 22px;
    border: 2px solid #00000044;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    cursor: pointer;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# 🎤 Voice function
def listen_to_user():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Speak now...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            st.write("🗣️ You said:", query)
            return query
        except:
            return "Sorry, I could not understand."

# 🤖 Ask ChatGPT as travel guide with short and travel-only answers
def ask_chatgpt(prompt):
    system_message = """
    You are Zippy, a cheerful and smart travel guide.
    Only answer travel-related questions clearly and shortly.
    Give easy-to-understand info suitable for travelers.
    If someone asks about a city, list the best 5 places to visit briefly.
    Never answer questions that are not about traveling.
    Keep answers friendly, simple, and 2-3 sentences long.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

# 🔈 Text to Speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# 🌐 Title and subtitle
st.markdown("<h1 style='text-align: center;'>🌍 World Travel Guide</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Say Hi to <strong>Zippy</strong> – Let’s Plan Your Next Getaway!</h3>", unsafe_allow_html=True)

# 🎙️ Button in center
st.markdown('<div class="center">', unsafe_allow_html=True)
if st.button("🎙️ Tap to Speak with Zippy"):
    user_question = listen_to_user()
    if user_question != "Sorry, I could not understand.":
        answer = ask_chatgpt(user_question)
        st.markdown(f"### ✈️ Zippy says:\n> {answer}")
        speak(answer)
    else:
        st.markdown(f"### ⚠️ {user_question}")
        speak(user_question)
st.markdown('</div>', unsafe_allow_html=True)
