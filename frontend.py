import pickle
from pathlib import Path
import streamlit as st
import requests
import time
import streamlit_authenticator as stauth

# Load backend API URL dynamically
BACKEND_URL = "https://think-tank-bot9-f6fhdpggfyexezgw.southafricanorth-01.azurewebsites.net/"

# Set up basic page configuration
st.set_page_config(page_title="Think Tank AI Chatbot", page_icon="🤖", layout="wide")

#  Full refresh approach using JavaScript
def force_refresh():
    """Injects JavaScript to refresh without delay."""
    st.write(
    """
    <script>
        window.location.href = window.location.href;
    </script>
    """,
    unsafe_allow_html=True
)

# --- USER AUTHENTICATION ---
names = ["Wade Kelden"]
usernames = ["wadek"]

# Load hashed passwords from file
file_path = Path(__file__).parent / "hashed_pw.pk1"

if file_path.exists():
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)
else:
    st.error(" Missing hashed_pw.pk1. Ensure it's deployed to Azure.")

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "sales_dashboard", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username or password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # Page title and welcome message
    st.title("Think Tank AI Enterprise Document Analysis Chatbot")
    st.markdown("**Welcome! Upload documents and engage with AI-generated insights.**")

    # Sidebar with branding and usage instructions
    with st.sidebar:
        st.image("tt.png", width=180)  # Project logo
        st.markdown("## 🤖 About Think Tank AI")
        st.markdown("""
        **Think Tank AI** simplifies document analysis for **Sales Teams**.  
        Upload a document, select a structured prompt, and engage dynamically!

        ###  **How to Use Think Tank AI**
        1️⃣ **Upload a document** (PDF format).  
        2️⃣ **Pick a pre-built prompt** to get started.  
        3️⃣ **Review AI insights**—summaries, checklists, action items.  
        4️⃣ **Ask follow-up questions** using the chat input box!  
        5️⃣ **Scroll through past conversations** to reference AI responses.

        **Restarting Your Conversation**
        
         Click **"Start New Conversation"** at the bottom.  
         **If the page does not refresh immediately, click twice.**  
         This ensures a full reset while keeping your document loaded.

        ###  **Why Use Think Tank AI?**
         **Saves time**—avoids manual scanning.  
         **Structured conversation**—pre-built prompts guide users.  
         **Unlimited Q&A**—continuous engagement.  
         **Designed for Sales Teams**—streamlines decision-making.

         **Get started now! Upload a document & unlock key insights effortlessly!**
        """)

    # Ensure session state is initialized
    if "doc_text" not in st.session_state:
        st.session_state.doc_text = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "used_prompts" not in st.session_state:
        st.session_state.used_prompts = []
    if "prompt_shown" not in st.session_state:
        st.session_state.prompt_shown = False  #  Tracks if first prompt selection was shown

    # Document upload section
    st.markdown("### 📄 Upload a Document")
    uploaded_doc = st.file_uploader("Upload your document (PDF Format)", type=["pdf", "txt"])

    if uploaded_doc and st.button("Extract & Load Document"):
        with st.spinner("Uploading and analyzing..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/extract_text",
                    files={"file": uploaded_doc}
                )
                result = res.json()
                st.session_state.doc_text = result["text"]
                st.session_state.chat_history = []  # Reset history
                st.success(" Document loaded! You can now ask questions.")

            except Exception as e:
                st.error(f"Error: {str(e)}")
    time.sleep(2)
    # Display chat history to ensure conversations remain visible
    if st.session_state.doc_text:
        # st.markdown("###  Conversation History")
        for message in st.session_state.chat_history:
            st.chat_message(message["role"]).markdown(message["content"])

        # Pre-built prompts for first interaction, **only after document is uploaded**
        
        def display_prompts():
            """Function to show prompts only for the first interaction."""
            if not st.session_state.prompt_shown:  #  Show heading **only once**
                st.markdown("### Choose Your First Question:")
                st.session_state.prompt_shown = True  #  Prevents heading from appearing again

            remaining_prompts = [
                " What are the key takeaways from this document?",
                " Please provide me with a checklist for success",
                " List the key action items based on this document."
            ]
            
            available_prompts = [prompt for prompt in remaining_prompts if prompt not in st.session_state.used_prompts]

            if available_prompts:
                cols = st.columns(len(available_prompts))  #  Dynamically adjust column count
                for i, prompt in enumerate(available_prompts):
                    if cols[i].button(prompt):  #  Avoids unpacking issues when less than 3 prompts remain
                        st.session_state.used_prompts.append(prompt)  #  Track used prompt
                        return prompt  #  Return selected prompt

            return None  # Once first prompt is chosen, don’t show prompts again

        selected_prompt = display_prompts()

        #  Use `st.chat_input` for follow-up questions
        user_question = st.chat_input(" Ask another question about the document:")

        if selected_prompt or user_question:
            query = user_question if user_question else selected_prompt
            st.session_state.chat_history.append({"role": "user", "content": query})

            with st.chat_message("user"):
                st.markdown(query)

            # Send conversation history to backend
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/followup_chat",
                        json={"doc": st.session_state.doc_text, "history": st.session_state.chat_history}
                    )
                    result = res.json()
                    ai_response = result["answer"]

                    #  Store and display AI response
                    message_placeholder.markdown(ai_response)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

                except Exception as e:
                    message_placeholder.markdown(f"Error: {str(e)}")

            st.markdown("---")
            

        
        if st.button(" Start New Conversation"):
        #  Remove all messages from the chat interface
            st.session_state.chat_history = []  # Clears chat history entirely

            #  Force full browser refresh to ensure clean UI
            st.write("""
                <script>
                    window.location.reload(true);
                </script>
            """, unsafe_allow_html=True)

                

