from groq import Groq
import os
import streamlit as st
 
 
def show_chat(weather_data):
    if "messages" not in st.session_state:
        st.session_state.messages = []
 
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
 
    question = st.chat_input("Ask about the weather data")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)
 
        try:
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system",
                     "content": ("Answer questions using only this weather data. "
                                 "You can give opinions or advice based on the data, like whether it is good weather for an activity. "
                                 "If the answer is not in the data, say so.\n"
                                 + weather_data.to_string(index=False))}
                ] + st.session_state.messages,
                reasoning_effort="low"
            )
            answer = response.choices[0].message.content
        except Exception:
            answer = "Sorry, the chat is not available right now."
 
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)
 