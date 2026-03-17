# Resume Analyzer

A resume analysis tool powered by the Claude API. Supports both a CLI interface and a FastAPI REST API server.

## Features

- Extracts text from PDF resumes
- Matches resume against a job description (optional)
- Provides skill match analysis, missing keywords, and improvement suggestions
- CLI mode: saves analysis output to `output.txt`
- API mode: exposes REST endpoints for integration with other services
- Frontend mode: web UI to upload a resume and optionally match against a job description

## Requirements

- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Usage

### CLI

```bash
# Analyze resume only
python resume_analyzer.py resume.pdf

# Analyze resume against a job description
python resume_analyzer.py resume.pdf job.txt
```

Results are saved to `output.txt`.

### Frontend (React)

A React web UI is included in the `resume-frontend/` directory.

**Start the frontend:**

```bash
cd resume-frontend
npm install
npm start
```

The app runs at `http://localhost:3000` and provides two modes:

- **Analyze**: Upload a PDF resume and click "Analyze" to get a standalone analysis (core skills, job directions, strengths, and improvements).
- **Match with JD**: Upload a PDF resume, paste a job description into the text box, and click "Match with JD" to get a match report (matched skills, missing keywords, suggested edits).

> Make sure the FastAPI backend is running (`uvicorn api:app --reload`) before using the frontend.

### API Server

Start the FastAPI server:

```bash
uvicorn api:app --reload
```

The server runs at `http://localhost:8000` with two endpoints:

#### `POST /analyze`

Upload a PDF resume for standalone analysis. Returns a structured summary including core tech stack, suitable job directions, resume strengths, areas to improve, and missing keywords for MLOps Engineer roles.

```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@resume.pdf"
```

#### `POST /match`

Upload a PDF resume and a job description to get a match analysis: matched skills, missing keywords, and suggested resume edits.

```bash
curl -X POST http://localhost:8000/match \
  -F "file=@resume.pdf" \
  -F "jd=Your job description text here"
```

Both endpoints return JSON: `{ "result": "<analysis text>" }`

## Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
