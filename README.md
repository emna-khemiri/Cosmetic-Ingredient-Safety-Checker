# Cosmetic Ingredient Safety Checker

A simple web application to check the safety status of cosmetic ingredients based on the EU COSING database, using ChromaDB for vector search and the Gemini API for safety explanations.

## Overview
This project provides a tool to query cosmetic ingredients and retrieve their safety status (e.g., prohibited, restricted, allowed) under EU regulations. It features:
- **Backend**: A FastAPI server that integrates ChromaDB for storing COSING data and the Gemini API for generating safety explanations.
- **Frontend**: A sleek, modern UI built with plain HTML, CSS, and JavaScript, featuring a glassmorphic card design with a centered layout and a dark blue theme.

## Features
- Search for ingredients and view their safety status.
- Built with FastAPI, ChromaDB, and the Gemini API.

## Prerequisites
- Python 3.8+
- Node.js (optional, for development tools)
- A Gemini API key (set in `.env`)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/cosmetic-safety-checker.git
cd cosmetic-safety-checker
```

### 2. Backend Setup
1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in `backend/` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn app:app --reload --port 8000
   ```

### 3. Frontend Setup
1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Serve the `index.html` file using a simple HTTP server:
   ```bash
   python -m http.server 3000
   ```
3. Open `http://localhost:3000` in your browser.

## Usage
1. Ensure the backend server is running on `http://localhost:8000`.
2. Open the frontend at `http://localhost:3000`.
3. Enter an ingredient name (e.g., "salicylic acid") in the input field and click "Check".
4. View the safety status and details in the results area.

## Project Structure
```
cosmetic-safety-checker/
├── backend/
│   ├── app.py                  # FastAPI server
│   ├── config.py               # Configuration loader
│   ├── data_loader.py          # COSING data loader
│   ├── chromadb_manager.py     # ChromaDB manager
│   ├── prompt_builder.py       # Prompt generator for Gemini API
│   ├── safety_checker.py       # Safety checker with Gemini API
│   ├── requirements.txt        # Backend dependencies
│   └── .env                    # Environment variables (not tracked)
├── frontend/
│   └── index.html              # Frontend UI (HTML/CSS/JS)
└── README.md                   # Project documentation
```

## Deployment

### Backend
- Deploy on Render or Heroku:
  1. Push the `backend/` folder to a Git repository.
  2. Set the `GEMINI_API_KEY` environment variable in your hosting platform.
  3. Configure the start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`.

### Frontend
- Deploy on Netlify or Vercel:
  1. Upload the `frontend/index.html` file.
  2. Update the `fetch` URL in the `<script>` tag to your deployed backend URL (e.g., `https://your-backend.onrender.com/check`).



## License
This project is licensed under the MIT License.

## Acknowledgments
- Built with [FastAPI](https://fastapi.tiangolo.com/), [ChromaDB](https://www.trychroma.com/), and the [Gemini API](https://ai.google.dev/).
- COSING database for ingredient safety data.
