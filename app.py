import streamlit as st
from agent import ask_agent

st.set_page_config(page_title="Ayyoon AI Assistant", page_icon="🤖")
st.title("🤖 Ayyoon AI Assistant")
st.write("Ask me about the weather, news, or any question!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_agent(prompt)
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})