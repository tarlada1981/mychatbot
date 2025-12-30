import streamlit as st
from groq import Groq
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="Kiran T. | AI Portfolio",
    page_icon="☁️",
    layout="wide"
)

# 2. Setup Groq Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ SRE Alert: GROQ_API_KEY not found in Streamlit Secrets.")
    st.stop()

# 3. Sidebar: Profile & Model Selector
with st.sidebar:
    try:
        st.image("profile.jpg", use_container_width=True)
    except:
        st.info("📷 profile.jpg not found.")
    
    st.title("Kiran T.")
    st.write("Senior SRE & Program Manager")
    
    st.divider()
    
    # --- MODEL SELECTOR DROPDOWN ---
    st.subheader("🤖 Brain Settings")
    model_options = {
        "Llama 3.3 70B (Powerhouse)": "llama-3.3-70b-versatile",
        "Llama 3.1 8B (Instant)": "llama-3.1-8b-instant",
        "Llama 3.2 3B (Efficient)": "llama-3.2-3b-preview"
    }
    
    selected_model_name = st.selectbox(
        "Select AI Model:",
        options=list(model_options.keys()),
        index=0,
        help="Llama 3.3 70B is best for complex logic. 8B is near-instant."
    )
    selected_model_id = model_options[selected_model_name]
    
    st.divider()
    st.caption(f"🟢 Engine: {selected_model_name}")

# 4. Load Resume Context
try:
    with open("resume.txt", "r") as f:
        resume_data = f.read()
except FileNotFoundError:
    st.error("⚠️ resume.txt missing.")
    st.stop()

# 5. Chat Interface
st.header("💬 Chat with my Professional AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask me about my SRE experience..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        sys_msg = (
            f"You are a professional hiring assistant for Kiran. "
            f"Use this resume to answer: {resume_data}. "
            "Be professional and concise."
        )

        try:
            # Use the ID from the sidebar selector
            completion = client.chat.completions.create(
                model=selected_model_id,
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )
            
            full_res = st.write_stream(completion)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            st.error(f"Inference Error: {e}")
            st.info("Try switching to a different model in the sidebar.")
