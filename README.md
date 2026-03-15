# Resume Analyzer

A CLI tool that uses the Claude API to analyze a resume (PDF) against a job description and provide actionable feedback.

## Features

- Extracts text from PDF resumes
- Matches resume against a job description (optional)
- Provides skill match analysis, missing keywords, and improvement suggestions
- Saves analysis output to `output.txt`

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

```bash
# Analyze resume only
python resume_analyzer.py resume.pdf

# Analyze resume against a job description
python resume_analyzer.py resume.pdf job.txt
```

Results are saved to `output.txt`.

## Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
