# Full-Stack AI Summarizer Application

This project is a small full-stack application built to fulfill the requirements of the recruitment exercise. It uses a Vue.js/TypeScript frontend to send text to a FastAPI/Python backend, which in turn gets a summary from the Google Gemini API.

---

## How to Run the Application

It is recommended to use a new virtual environment for the backend to avoid dependency conflicts.

### 1. Backend Setup

First, set up and run the FastAPI server.

```shell
# 1. Navigate to the backend directory

# 2. (Recommended) Create and activate a new Python environment

# 3. Install dependencies from the lock file
pip install -r requirements.txt

# 4. Set up the Gemini API Key
#    - Rename .env.example to .env
#    - Add your Gemini API Key to the .env file

# 5. Run the development server
uvicorn main:app --reload
```

The backend API will now be running on `http://127.0.0.1:8000`.

### 2. Frontend Setup

In a **separate terminal**, set up and run the Vue.js frontend.

```shell
# 1. Navigate to the frontend directory

# 2. Install dependencies
npm install

# 3. Run the development server
npm run dev
```

The frontend application will now be running on `http://localhost:5173`. You can open this URL in your browser to use the application.

---

## How to Run the Tests

The unit tests for the backend can be run using `pytest`.

```shell
# 1. Navigate to the backend directory

# 2. (Ensure your environment is activated and dependencies are installed)

# 3. Run pytest
pytest -v
```

