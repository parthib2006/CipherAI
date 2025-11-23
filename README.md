# CipherAI — DFIR Agent Orchestrator  
Powered by Google Gemini + ADK + Streamlit

CipherAI is an automated DFIR (Digital Forensics & Incident Response) analysis  
tool that processes Logs, PCAP JSON, and Memory Artefacts using Google Gemini  
agents.  
It produces a clean forensic summary and a downloadable PDF report with charts.

---

## 🚀 Features

- Multi-agent DFIR pipeline (Log + PCAP + Memory Analysis)
- ADK Orchestrator for reliable inference
- PDF report generation with graphs
- Streamlit frontend with file-upload support
- API key validation step
- Fully deployable to Streamlit Cloud

---

## 🔧 Installation

Clone the repository:


Install dependencies:

`pip install -r requirements.txt`

---

## 🔑 Environment Setup

Create a `.env` file:
`GEMINI_API_KEY="your_api_key_here"`


Never commit `.env` to GitHub.

---

## ▶️ Running the Streamlit App

`streamlit run app.py`

---

text
```
📁 CipherAI/
|
│── LICENSE
│── README.md
|── requirements.txt
│── core/
│   └── agents.py
|   |── orchestrator.py
|   |── report_generator.py
|   |── utils.py
│── app.py
│── utils.py
│── .gitignore
```


## 📄 License

MIT License
