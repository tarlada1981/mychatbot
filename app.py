import streamlit as st
from groq import Groq
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Kiran T. | AI Portfolio", page_icon="🤖", layout="wide")

# 2. Setup Groq Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ GROQ_API_KEY missing in Streamlit Secrets.")
    st.stop()

# 3. Sidebar: Profile & Model Settings
with st.sidebar:
    try:
        st.image("profile.jpg", use_container_width=True)
    except:
        st.info("📷 profile.jpg not found.")
    
    st.title("Kiran T.")
    st.write("Senior SRE & Program Manager")
    st.divider()
    
    st.subheader("⚙️ Model Settings")
    model_options = {
        "Llama 3.3 70B (Recommended)": "llama-3.3-70b-versatile",
        "Llama 3.1 8B (Fast)": "llama-3.1-8b-instant"
    }
    selected_model = st.selectbox("Choose AI Brain:", options=list(model_options.keys()))
    model_id = model_options[selected_model]

# 4. Load Resume Text
try:
    with open("resume.txt", "r") as f:
        resume_data = f.read()
except FileNotFoundError:
    st.error("resume.txt not found. Please upload it to GitHub.")
    st.stop()

# 5. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Helper Function to Fix the Chunk Error ---
def generate_groq_response(response):
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# 6. Interaction Logic
if prompt := st.chat_input("Ask about my professional background..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Request the stream from Groq
            raw_stream = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant for Kiran. Answer using this resume: {resume_data}"},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )
            
            # Pass our generator to st.write_stream to get clean text
            full_response = st.write_stream(generate_groq_response(raw_stream))
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Inference Error: {e}")
