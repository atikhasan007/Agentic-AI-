
# LangGraph Chatbot with Google Gemini (Memory Enabled)

This project is a simple conversational AI chatbot built using LangGraph, LangChain, and Google Gemini (Generative AI). It supports in-memory conversation persistence using MemorySaver.

---

## Features

- Built with LangGraph StateGraph architecture
- Uses Google Gemini (gemini-3.1-flash-lite)
- Maintains chat history using message state
- In-memory persistence using MemorySaver
- Lightweight and fast execution
- Node-based modular design

---

## Architecture Flow

START → chat_node → END

User message → State → Gemini LLM → Response → Updated State

---

<img width="945" height="776" alt="image" src="https://github.com/user-attachments/assets/4795c71c-2a08-4de1-9f7f-2f3dd7ff3706" />
