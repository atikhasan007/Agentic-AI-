import os
import certifi 
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import create_react_agent , AgentExecutor 


# load env variables
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY=os.getenv("WEATHERSTACK_API_KEY")


st.set_page_config(
    page_title="Agentic AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Agentic AI Assistant")
st.markdown("Search + Weather AI Agent using LangChain")




# SEARCH TOOL
# ==========================================
search_tool = TavilySearchResults(max_results=2)


# WEATHER TOOL
# ==========================================
@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    url = (
        f"http://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )

    response = requests.get(url)

    data = response.json()

    if "current" not in data:
        return f"Could not fetch weather data for {city}"

    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )




# llm 
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


# prompt -< pre existing 
prompt = hub.pull("hwchase17/react")



# tools 
tools = [search_tool, get_weather_data]



# create agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# Executor

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)




# ==========================================
# SIMPLE THEME COLOR (ONLY STYLE CHANGE)
# ==========================================
st.markdown(
    """
    <style>
    /* Background */
    .stApp {
        background-color: #0f172a;
        color: white;
    }

    /* Input box */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: white;
        border-radius: 8px;
        border: 1px solid #334155;
    }

    /* Button */
    .stButton > button {
        background-color: #22c55e;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        border: none;
    }

    .stButton > button:hover {
        background-color: #16a34a;
        color: white;
    }

    /* Success box */
    .stAlert {
        background-color: #1e293b;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# UI INPUT
# ==========================================

user_query = st.text_input(
    "Enter your query:",
    placeholder="Example: Find the capital of India and current weather"
)

# ==========================================
# RUN AGENT
# ==========================================

if st.button("Run Agent"):

    if user_query:

        with st.spinner("Agent is thinking..."):

            try:
                response = agent_executor.invoke({
                    "input": user_query
                })

                st.success("Response Generated")

                st.markdown("## Final Response")
                st.write(response["output"])

            except Exception as e:
                st.error(f"Error: {str(e)}")

    else:
        st.warning("Please enter a query")