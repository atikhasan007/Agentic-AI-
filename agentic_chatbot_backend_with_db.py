from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict , Annotated
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
import sqlite3
import operator
import os 


# loading 
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# llm 
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)




class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]



def chat_node(state: ChatState):
    #take user query from state
    messages = state['messages']
    # send to llm
    response = llm.invoke(messages)
    # response store state
    return {'messages': [response]}



conn= sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpoint = SqliteSaver(conn)  # for persistance inside the db





graph = StateGraph(ChatState)
# add nodes
graph.add_node('chat_node', chat_node)
#add edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)


chatbot = graph.compile(checkpointer=checkpoint) # store in ram 



def get_all_thread():
    all_threads = set()
    for ckpt in checkpoint.list(None):
        all_threads.add(ckpt.config['configurable']['thread_id'])


    return list(all_threads)



# CONFIG = {'configurable': {
#     'thread_id':'default_thread-1'
# }}


# res = chatbot.invoke(
#     {
#         "messages": [
#             HumanMessage(content="my name is arik.what is python?")
#         ]
#     },
#     config=CONFIG
# )

# print(res)