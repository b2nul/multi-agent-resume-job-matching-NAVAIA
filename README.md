# Resume & Job Matching Assistant — NavaiaForge Workforce

A 4-agent AI workforce built with the [NavaiaForge SDK](https://fareegi.navaia.sa) that takes a resume and produces a structured skills breakdown, ranked job matches, a gap analysis, and a tailored cover letter for the best-fit role.

Built as the NavaiaForge SDK technical assessment (AI Engineer Intern track): run a backend locally, assemble a multi-agent workforce via the SDK, run it, sync it to the cloud, and publish it to the marketplace.

## What it does

Given a resume, the workforce runs a linear pipeline:

```
Resume Analyzer  →  Job Search Agent  →  Matching Agent  →  Application Agent
```

1. **Resume Analyzer** — extracts technical and soft skills, work experience, education, projects, and an overall candidate level.
2. **Job Search Agent** — finds 5–8 relevant roles, focused on the Saudi tech/AI market (SDAIA, STC, Mobily, Aramco, NEOM, etc.) plus strong remote roles.
3. **Matching Agent** — scores each job (0–100), identifies skill gaps and strengths, and gives an Apply / Consider / Skip recommendation, ranked highest to lowest.
4. **Application Agent** — writes a tailored cover letter for the top match, plus a short follow-up email template.

## Why this design

A linear pipeline mirrors how a real job search actually flows — you can't match jobs before understanding the resume, and you can't write a targeted cover letter before knowing which role is the best fit. Each agent has a single, clear responsibility, which keeps outputs focused and the system easy to debug and extend.

## Tech

- **NavaiaForge SDK** (`navaia-forge`) — workforce, agent, edge, task, and sync/publish orchestration
- **Backend** — runs locally via Docker (FastAPI + Postgres + Weaviate + Redis)
- **Models** — served through OpenRouter (configurable; runs on a free model by default)

## Project structure

| File | Purpose |
|------|---------|
| `run_workforce.py` | Builds the workforce + 4 agents, wires the pipeline, runs a sample task |
| `new_key.py` | Registers/logs in and mints a local API key |
| `publish.py` | Syncs the workforce to the cloud and publishes it to the marketplace |
| `check_status.py` | Checks the published workforce's moderation status |

## Running it

1. Start the local backend (Docker) and confirm `http://localhost:8001/health` is healthy.
2. Get a local API key (`new_key.py`) and an OpenRouter API key.
3. Fill in your keys in `run_workforce.py`, then `python run_workforce.py` to build and run.
4. Fill in your cloud key in `publish.py`, then `python publish.py` to sync and publish.

> **Note:** API keys and secrets are kept in a local `.env` file and out of source control (see `.gitignore`). Replace the placeholder key values in the scripts with your own.

## Notes

The local setup required resolving several environment and schema issues to get a clean end-to-end run (environment variables, database migrations and tables, an SDK auth-header detail on key creation, and a runtime-mode value). The workforce runs end to end and was published to the NavaiaForge marketplace.

## AI tools

I used an AI assistant to help design the agent roles and instructions, and to debug the local setup issues above. The final structure, decisions, and testing are my own.
