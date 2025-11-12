# 🧮 Insurance Premium Predictor (Learning Project)

This is a **learning project** built while exploring **FastAPI** and **Streamlit**.  
It demonstrates how to build a simple machine learning app with a backend API and a frontend interface, both containerized using Docker.

> ⚠️ Note: The prediction results are **not highly reliable** since the model was trained on a small dataset — this project was made for learning purposes only.

---

## 🚀 What This App Does
- Uses a basic ML model (`model.pkl`) to predict an insurance premium category  
- FastAPI serves as the backend API (`app.py`)  
- Streamlit provides a simple web UI (`frontend.py`)  
- Docker ensures it runs consistently on any machine

---

## 🧩 Tech Stack
- **Python 3.11**
- **FastAPI**
- **Streamlit**
- **scikit-learn**
- **Docker**

---
⚙️ Running Locally
1️⃣ Backend (FastAPI)

# Install dependencies
pip install -r requirements.txt

# Run FastAPI
uvicorn app:app --reload

2️⃣ Frontend (Streamlit)

In another terminal:

# Run the Streamlit frontend
streamlit run frontend.py

🐳 Running with Docker
1️⃣ Build the Docker image
docker build -t your_username/insurance-premium-prediction .

2️⃣ Run the container
docker run -p 8000:8000 your_username/insurance-premium-prediction
