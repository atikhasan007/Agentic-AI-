from agentic_chatbot_langgraph_backend import chatbot
from langchain_core.messages import  HumanMessage
import streamlit as st
import uuid

st.title("Agentic Chatbot with LangGraph")


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())


CONFIG = {
    "configurable": {
        "thread_id": st.session_state["thread_id"]
    }
}

# session state like a dictionary 
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
# loading the conversion history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])





user_input = st.chat_input("Type here...")

if user_input:
    ##addition line for session state
    ## first add the message to message_history
    st.session_state['message_history'].append({
        'role':'user',
        'content':user_input
    })
    with st.chat_message('user'):
        st.text(user_input)
    


    # one shot ouput

    # response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    # result = response['messages'][-1].content
    # ai_message = result[0]['text']
    # # first add the message to message_history
    # st.session_state['message_history'].append({
    #     'role':'assistant',
    #     'content':ai_message
    # })
    # with st.chat_message('assistant'):
    #     st.text(ai_message)





    # first add the message to message_history
    # streaming output

    with st.chat_message("assistant"):

        def generate_text():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                content = message_chunk.content

                # content is list
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            yield item.get("text", "")

                # content is string
                elif isinstance(content, str):
                    yield content

        ai_message = st.write_stream(generate_text())

        st.session_state["message_history"].append({
            "role": "assistant",
            "content": ai_message
        })