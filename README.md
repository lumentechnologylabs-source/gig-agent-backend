# Gig Agent (MVP)

A tiny agent that fetches remote/freelance gigs from a few public sources,
scores them against your skills and preferences, and outputs a ranked list.
It exposes both a CLI and a small FastAPI service.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Copy and edit your settings
# Copy and edit your settings

# macOS / Linux
cp .env.example .env

# Windows (PowerShell)
copy .env.example .env';

# Run once from the CLI
python -m gig_agent.cli --limit 25 --out gigs.json

# Or run the API
uvicorn app.main:app --reload

# Or with Docker
docker build -t gig-agent .
docker run --rm -p 8000:8000 --env-file .env gig-agent
```
