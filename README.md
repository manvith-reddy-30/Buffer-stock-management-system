
---

```markdown
# 🧊 Buffer Stock Management System

A smart agricultural decision support system that predicts tomato prices, analyzes weather trends, and generates buffer stock reports for districts in **Telangana**, India. It combines **AI forecasting**, **weather-aware insights**, and **interactive web UI**.

---

## 🌐 Live Districts

- 📍 **Warangal**
- 📍 **Hyderabad**
- 📍 **Nalgonda**
- 📍 **Rangareddy**
- 📍 **Medak**

---

## 🚀 Features

### 🧠 Backend
- ✅ LSTM-based tomato price forecasting (7-day horizon)
- ✅ Weather forecast generation using LLM agents (Google GenAI)
- ✅ District-level buffer stock analysis using Gemini models
- ✅ FastAPI backend with clean REST endpoints
- ✅ Interactive Swagger UI for testing (`/docs`)

### 🎯 Frontend
- ✅ Modern React UI for entering prices and uploading stock
- ✅ Real-time district selection and form validation
- ✅ Toast-based feedback using `react-toastify`
- ✅ Communicates with FastAPI backend for reports

---

## 🧱 Project Structure

```

Buffer-stock-management-system/
├── backend/
│   ├── inference/               # LSTM price prediction logic
│   ├── report/                  # AI-generated reports per district
│   ├── agents/                  # Weather agents for LLM sessions
│   ├── models/                  # Saved scalers and LSTM models
│   ├── test\_inference.py        # Pytest unit tests
│   ├── test\_app.py              # FastAPI app (entry point)
│   └── .env                     # API keys and model configs
├── frontend/
│   ├── src/
│   │   ├── components/          # React components (forms, cards)
│   │   └── App.jsx              # Main App UI
│   └── public/                  # Static files
├── README.md
└── requirements.txt

````

---

## 🔧 Setup Instructions

### 🖥️ Backend Setup (FastAPI + GenAI)

1. Navigate to backend:
   ```bash
   cd backend
````

2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Add `.env` in `backend/`:

   ```env
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY="your gemini api key"
    MODEL = "gemini-2.0-flash-exp"
   DATABASE_URL="postgresql db url"
   ```

5. Run the server:

   ```bash
   uvicorn test_app:app --reload --port 9000
   ```

6. Access API at: [http://localhost:9000/docs](http://localhost:9000/docs)

---

### 🌍 Frontend Setup (React)

1. Navigate to frontend:

   ```bash
   cd frontend
   ```

2. Install frontend dependencies:

   ```bash
   npm install
   ```

3. Start development server:

   ```bash
   npm run dev
   ```

4. Access UI at: [http://localhost:3000](http://localhost:3000)

> ⚠️ Ensure backend is running on port `9000` before triggering report actions from frontend.

---

## 📬 API Endpoints (FastAPI)

### 📊 Report Generation

| Endpoint                    | Description                     |
| --------------------------- | ------------------------------- |
| `POST /analysis/warangal`   | Generates report for Warangal   |
| `POST /analysis/hyderabad`  | Generates report for Hyderabad  |
| `POST /analysis/nalgonda`   | Generates report for Nalgonda   |
| `POST /analysis/rangareddy` | Generates report for Rangareddy |
| `POST /analysis/medak`      | Generates report for Medak      |

Each takes JSON with:

```json
{
  "warangal_last_week_actual": [...],
  "warangal_next_week_pred": [...],
  ...
  "buffer_quantity": {
    "warangal": 20,
    "hyderabad": 15,
    ...
  }
}
```

---

## ✅ Testing Backend

Run Pytest tests for LSTM prediction:

```bash
cd backend
pytest test_inference.py
```

---

## 🧪 Tools Used

* 🧠 Google ADK + gemini-2.0-flash-exp
* ⚙️ TensorFlow / Keras
* 📦 FastAPI
* 💻 ReactJS
* 🧪 Pytest
* ☁️ `.env` for key security
* 🍅 LSTM forecasting models per district

