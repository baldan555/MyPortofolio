import streamlit as st
from typing import Generator
from groq import Groq

def main():
    # Define model details
    models = {
        "gemma2-9b-it": {"name": "Gemma2-9b-it", "tokens": 8192, "developer": "Google"},
        "llama-3.3-70b-versatile": {"name": "LLaMA3.3-70b-versatile", "tokens": 128000, "developer": "Meta"},
        "llama-3.1-8b-instant": {"name": "LLaMA3.1-8b-instant", "tokens": 128000, "developer": "Meta"},
        "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
        "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
        "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
    }

    # Sidebar configuration
    with st.sidebar:
        st.header("Settings")
        
        model_option = st.selectbox(
            "Select Model",
            options=list(models.keys()),
            format_func=lambda x: f"{models[x]['name']} ({models[x]['developer']})",
            index=list(models.keys()).index("mixtral-8x7b-32768"),  # Default model
            key="model_select"
        )

        max_tokens_range = models[model_option]["tokens"]
        max_tokens = st.slider(
            "Max Tokens",
            min_value=512,
            max_value=max_tokens_range,
            value=min(32768, max_tokens_range),
            step=512,
            help=f"Max tokens for {models[model_option]['name']}: {max_tokens_range}",
            key="tokens_slider"
        )

    # Main content
    st.write(
        '<span style="font-size: 78px; line-height: 1">🏎️</span>',
        unsafe_allow_html=True,
    )
    st.subheader("Groq Chat Streamlit App", divider="rainbow", anchor=False)

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "mixtral-8x7b-32768"

    # Client initialization
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    # Detect model change
    if st.session_state.selected_model != model_option:
        st.session_state.messages = []
        st.session_state.selected_model = model_option

    # Chat history display
    for message in st.session_state.messages:
        avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Chat response generator
    def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
        for chunk in chat_completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    # Chat input
    if prompt := st.chat_input("Enter your prompt here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar='👨‍💻'):
            st.markdown(prompt)

        try:
            chat_completion = client.chat.completions.create(
                model=model_option,
                messages=[
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.messages
                ],
                max_tokens=max_tokens,
                stream=True
            )

            with st.chat_message("assistant", avatar="🤖"):
                chat_responses_generator = generate_chat_responses(chat_completion)
                full_response = st.write_stream(chat_responses_generator)
        except Exception as e:
            st.error(e, icon="🚨")

        if isinstance(full_response, str):
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            combined_response = "\n".join(str(item) for item in full_response)
            st.session_state.messages.append({"role": "assistant", "content": combined_response})

if __name__ == "__main__":
    main()
