import os
import streamlit as st
from groq import Groq
from groq import RateLimitError
# For some reason llama doesn't work and has been deprecated! Had to research and instead
# I'm using GPT!
#MODEL_NAME = "llama-3.1-8b-instant"
MODEL_NAME = "openai/gpt-oss-20b"
GREETING_TITLE = "IT Help Desk Bot"
GREETING_CAPTION = "You are chatting with an automated assistant, not a person."
INPUT_HELP = "What do you need help with?"
ERROR_MESSAGE_RATELIMIT = "The AI service is busy right now. Please wait and try again."
ERROR_MESSAGE_EXCEPTION = "The AI service is unavailable right now. Please try again later."

# Connect to Groq
client = Groq(api_key=os.environ["GROQ_API_KEY"])


# Tell the bot what it can do
SYSTEM_PROMPT = """
You are an IT Help Desk Assistant.

You can:
- Help with passwords.
- Help with Wi-Fi.
- Help with basic computer problems.

You must never:
- Pretend to be a human.
- Make up information.
- Answer questions unrelated to IT.

If a question is outside your job, say:
"Sorry, I can only help with IT questions."
"""



# Set up the page
st.title(GREETING_TITLE)

st.caption(GREETING_CAPTION)


# Store messages
if "messages" not in st.session_state:
    st.session_state.messages = []


# Show old messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get user input
user_input = st.chat_input(INPUT_HELP)


if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })


    # Show user message
    with st.chat_message("user"):
        st.write(user_input)


    # Keep the last 10 messages
    recent_messages = st.session_state.messages[-10:]


    # Get AI response
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=MODEL_NAME,

                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    }
                ] + recent_messages,

                stream=True
            )


            # Show response as it arrives
            reply = st.write_stream(
                chunk.choices[0].delta.content or ""
                for chunk in stream
            )


            # Save AI response
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        # Handle rate limits
        except RateLimitError:
            st.error(ERROR_MESSAGE_RATELIMIT)
        # Handle other errors
        except Exception:
            st.error(ERROR_MESSAGE_EXCEPTION)
        


