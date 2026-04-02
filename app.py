import streamlit as st
from anthropic import Anthropic

st.set_page_config(page_title="Smart Chatbot with Memory", page_icon="🧠")
st.title("🧠 Smart Chatbot with Memory")

client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

system_prompt = """
You are InterviewAce, a helpful interview preparation coach.

Rules:
- Only answer questions related to interviews, resumes, careers, and job preparation
- If the user asks something off-topic, politely say you focus on interview prep
- Give practical, structured, beginner-friendly answers
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_input_tokens" not in st.session_state:
    st.session_state.total_input_tokens = 0

if "total_output_tokens" not in st.session_state:
    st.session_state.total_output_tokens = 0

st.sidebar.header("Usage")
st.sidebar.write(f"Input tokens: {st.session_state.total_input_tokens}")
st.sidebar.write(f"Output tokens: {st.session_state.total_output_tokens}")

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
    st.session_state.total_input_tokens = 0
    st.session_state.total_output_tokens = 0
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=200,
            system=system_prompt,
            messages=st.session_state.messages
        )

        assistant_reply = response.content[0].text

        st.session_state.total_input_tokens += response.usage.input_tokens
        st.session_state.total_output_tokens += response.usage.output_tokens

        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"Error: {e}")