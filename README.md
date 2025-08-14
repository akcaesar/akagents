# Multi-Provider Summarization API

**Author:** Akshay NS  
**Description:**  
A modular, extensible summarization API supporting multiple backends such as **Ollama**, **LangChain**, and easily extendable to HuggingFace or any other LLM provider. Built with clean architecture principles and the Strategy Pattern for maximum flexibility.

---

## 📂 Project Structure
app/
│
├── domain/ # Business logic contracts
│ └── services/
│ └── summarization_service.py # Abstract interface for summarizers
│
├── infrastructure/ # External integrations
│ ├── ollama_clients/
│ │ └── ollama_summarizer.py # Ollama-based summarizer
│ ├── langchain_clients/
│ │ └── langchain_summarizer.py # LangChain-based summarizer
│ └── huggingface_clients/ # (Optional future)
│ └── hf_summarizer.py
│
├── application/ # Use cases
│ └── use_cases/
│ └── run_summarization.py # Orchestrates summarization
│
└── interfaces/ # API / CLI adapters
└── api/
└── routes/
└── summarize.py # FastAPI endpoint


---

## 🧠 Design Philosophy

This project follows **Clean Architecture** + **Strategy Pattern**.

- **Clean Architecture**
  - Domain layer defines **contracts** (`SummarizationService`).
  - Infrastructure layer provides **implementations** (Ollama, LangChain).
  - Application layer **uses** services without knowing provider details.
  - Interface layer (FastAPI) **adapts** to HTTP requests.

- **Strategy Pattern**
  - Multiple interchangeable summarizers implement the same interface.
  - Swapping from Ollama to LangChain requires no core code changes.
  - Runtime provider selection via **dependency injection**.

---




License
MIT License – free to use, modify, and distribute.