# import section 
from agentic_chatbot_backend_with_db import chatbot , get_all_thread


from langchain_core.messages import (
    HumanMessage,
    AIMessage
)
import streamlit as st
import uuid





# ==========================
# Utility Functions
# ==========================

# Generate Thread ID
def generate_thread_id():
    return str(uuid.uuid4())

# Get Config ন
def get_config():
    return {
        "configurable": {
            "thread_id": st.session_state["thread_id"]
        }
    }


# add thread তুন conversation list-এ যোগ করে।
def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


#Reset Chat
def reset_chat(): # নতুন chat শুরু করে।

    new_thread = generate_thread_id() # নতুন thread তৈরি।

    st.session_state["thread_id"] = new_thread # বর্তমান thread পরিবর্তন।

    st.session_state["message_history"] = [] # UI clear করে।

    add_thread(new_thread) # Sidebar list-এ add করে।



# Load Conversation
def load_conversation(thread_id): # LangGraph checkpointer থেকে conversation history load করে।
    # Checkpointer থেকে state নিয়ে আসে।
    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return state.values.get("messages", [])


# ==========================
# Session State Initialization
# ==========================

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# Checkpointer থেকে state নিয়ে আসে।
if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = get_all_thread()  # change for db


# Add current thread
add_thread(st.session_state["thread_id"])


# ==========================
# UI
# ==========================

st.title("Agentic Chatbot with LangGraph")


# ==========================
# Sidebar
# ==========================

st.sidebar.title("My Conversations")

if st.sidebar.button("➕ New Chat"):

    reset_chat()

    st.rerun()


for thread_id in reversed(st.session_state["chat_threads"]):

    if st.sidebar.button(
        f"Chat - {str(thread_id)[:8]}",
        key=thread_id
    ):

        st.session_state["thread_id"] = thread_id

        messages = load_conversation(thread_id)

        temp_messages = []

        for message in messages:

            if isinstance(message, HumanMessage):

                temp_messages.append(
                    {
                        "role": "user",
                        "content": message.content
                    }
                )

            elif isinstance(message, AIMessage):

                content = message.content

                if isinstance(content, list):

                    text = ""

                    for item in content:

                        if isinstance(item, dict):
                            text += item.get("text", "")

                        else:
                            text += str(item)

                    content = text

                temp_messages.append(
                    {
                        "role": "assistant",
                        "content": content
                    }
                )

        st.session_state["message_history"] = temp_messages

        st.rerun()


# ==========================
# Display Messages
# ==========================

for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================
# Chat Input
# ==========================

user_input = st.chat_input("Type your message...")


if user_input:

    # Save user message

    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Show user message

    with st.chat_message("user"):

        st.markdown(user_input)

    # Assistant response

    with st.chat_message("assistant"):

        def generate_text():

            for message_chunk, metadata in chatbot.stream(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=get_config(),
                stream_mode="messages"
            ):

                content = message_chunk.content

                # Gemini format

                if isinstance(content, list):

                    for item in content:

                        if isinstance(item, dict):

                            text = item.get("text", "")

                            if text:
                                yield text

                # OpenAI format

                elif isinstance(content, str):

                    yield content

        ai_message = st.write_stream(generate_text())

    # Save assistant response

    st.session_state["message_history"].append(
        {
            "role": "assistant",
            "content": ai_message
        }
    )