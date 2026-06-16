# LangChain AI Agent 

A minimal LangChain-based AI Agent project built for learning and experimentation.  
This project demonstrates how to build an agent using Python, LangChain, and GemeniAI API with external tool integration.

---

## 🚀 Features

- Simple LangChain agent setup
- Environment variable support using `.env`
- Multiple entry points (`app.py`, `main.py`)
- Research and experiments using Jupyter Notebook
- Integration with external APIs (Tavily, WeatherStack)

---

## 🛠️ Tech Stack

- Python 3.11
- LangChain
- GemeniAI API
- Tavily API
- WeatherStack API
- python-dotenv

---

## 📂 Project Structure

LangChain-AI-Agent/
│
├── app.py # Main application
├── main.py # Alternative entry point
├── requirements.txt # Dependencies
├── .env # API keys (not pushed to GitHub)
│
└── research/
└── agent_demo.ipynb # Experiments & research



---

## ⚙️ Installation

### 1. Create environment
```bash
conda create -n sima python=3.11 -y
conda activate sima

pip install -r requirements.txt
```

## Environment Setup

```bash
GIMINI_API_KEY="your-gemeni-api-key"
TAVILY_API_KEY="your-tavily-api-key"
WEATHERSTACK_API_KEY="your-weatherstack-api-key"
```

# Run Project
```bash
python app.py
python main.py
```

## Notebook
```bash
jupyter notebook research/agent_demo.ipynb
```
ui
<img width="997" height="582" alt="image" src="https://github.com/user-attachments/assets/677f85e2-ac27-46ae-86de-439ecf31be73" />

