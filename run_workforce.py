"""
NavaiaForge — Resume & Job Matching Assistant (4 agents)
Run order: Phase 3 (build) -> Phase 4 (run) -> Phase 5 (sync + publish)

Just run:  python run_workforce.py
"""

import time
from navaia_forge import NavaiaForgeClient

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
LOCAL_API_KEY = "nf_your_local_key_here"
CLOUD_API_KEY = "nf_your_cloud_key_here"

# Free model (no credits needed). If unavailable, swap for another :free model.
MODEL = "deepseek/deepseek-chat-v3-0324:free"

# Toggle: set to False on the first run to test build+run only (skip cloud).
DO_SYNC_AND_PUBLISH = False


# ─────────────────────────────────────────────
# CONNECT
# ─────────────────────────────────────────────
local = NavaiaForgeClient(base_url=LOCAL_BASE_URL, api_key=LOCAL_API_KEY)
print("Connected to local backend")


# ─────────────────────────────────────────────
# PHASE 3 — BUILD WORKFORCE + 4 AGENTS
# ─────────────────────────────────────────────
wf = local.workforces.create(
    name="Resume & Job Matching Assistant",
    runtime_mode="claude_max",
)
print(f"Workforce created — ID: {wf.id}")

resume_analyzer = local.agents.create(
    workforce_id=wf.id,
    name="Resume Analyzer",
    role="analyzer",
    instructions=(
        "You are an expert resume parser. Given a resume, extract a structured summary: "
        "1) Technical skills. 2) Soft skills. 3) Work experience (company, role, duration, achievements). "
        "4) Education (degree, institution, year, GPA). 5) Projects (name, tech, impact). "
        "6) Candidate level (Junior/Mid/Senior) with a one-line justification. "
        "Output clearly labeled sections. Note anything missing."
    ),
    model_provider="openrouter",
    model_name=MODEL,
)
print(f"  Resume Analyzer — {resume_analyzer.id}")

job_searcher = local.agents.create(
    workforce_id=wf.id,
    name="Job Search Agent",
    role="researcher",
    instructions=(
        "You are a job market specialist for the Saudi tech/AI market and global remote roles. "
        "Given a resume summary, list 5-8 relevant job opportunities. For each: job title, company, "
        "location, key requirements, and why it fits. Focus on data science, AI/ML, NLP, software "
        "engineering. Prioritize Saudi employers (SDAIA, STC, Mobily, Aramco, NEOM) plus strong remote roles. "
        "Base suggestions on realistic, known employers and role patterns."
    ),
    model_provider="openrouter",
    model_name=MODEL,
)
print(f"  Job Search Agent — {job_searcher.id}")

matcher = local.agents.create(
    workforce_id=wf.id,
    name="Matching Agent",
    role="analyst",
    instructions=(
        "You are a talent matching specialist. Given (A) the resume summary and (B) the job list, "
        "produce for each job: a Match Score (0-100), Skill Gaps, Strengths, and a Recommendation "
        "(Apply / Consider / Skip). Rank jobs highest to lowest. Be honest about gaps. "
        "Output a ranked table then detailed breakdowns."
    ),
    model_provider="openrouter",
    model_name=MODEL,
)
print(f"  Matching Agent — {matcher.id}")

application_writer = local.agents.create(
    workforce_id=wf.id,
    name="Application Agent",
    role="writer",
    instructions=(
        "You write compelling, personalized job applications. For the top-ranked job, write a cover letter: "
        "1) Strong specific hook (never 'I am writing to apply for'). 2) 2-3 concrete achievements matching "
        "the role. 3) Honest, positive framing of any gap. 4) Clear call to action. "
        "3-4 paragraphs, under 350 words. Then a short follow-up email template (under 100 words). "
        "Tailor everything to the specific job and company."
    ),
    model_provider="openrouter",
    model_name=MODEL,
)
print(f"  Application Agent — {application_writer.id}")

# Wire pipeline: Analyzer -> Searcher -> Matcher -> Writer
local.workforces.edges.create(workforce_id=wf.id, source_agent_id=resume_analyzer.id, target_agent_id=job_searcher.id)
local.workforces.edges.create(workforce_id=wf.id, source_agent_id=job_searcher.id, target_agent_id=matcher.id)
local.workforces.edges.create(workforce_id=wf.id, source_agent_id=matcher.id, target_agent_id=application_writer.id)
print("Pipeline wired: Analyzer -> Searcher -> Matcher -> Writer")


# ─────────────────────────────────────────────
# PHASE 4 — RUN A TASK
# ─────────────────────────────────────────────
SAMPLE_RESUME = """
Bayan Al-Harbi — CS Graduate (AI Track), King Abdulaziz University, Riyadh

EDUCATION: B.Sc. Computer Science (AI Track), King Abdulaziz University, 2024

SKILLS: Python, SQL, PyTorch, TensorFlow/Keras, HuggingFace, LangChain, LiteLLM,
FastAPI, Flask, MySQL, ChromaDB, Docker, Git, Label Studio. Arabic NLP, RAG, NER,
multi-agent systems, LSTM, transfer learning.

EXPERIENCE:
- NLP Data Engineer, Baiyyna (Tuwaiq Hackathon), 2024: annotated 12k+ Saudi court
  rulings, 11-entity NER schema, CAMeL-BERT+CRF model (F1 ~0.88), RAG integration.
- AI Intern, ACWA Power, 2023: predictive maintenance (PCA + KMeans), cut false
  positives 30%.

PROJECTS: SolarWay (LSTM solar prediction), Baiyyna (Arabic legal RAG+NER),
6-Agent Research Pipeline, Perfume Counterfeit Detection (YOLO+MobileNetV3),
G-Concierge (Arabic gov services RAG).

LANGUAGES: Arabic (native), English (professional).
"""

print("\nSubmitting task...")
task = local.tasks.create(
    workforce_id=wf.id,
    title="Resume analysis, job matching, and cover letter",
    description=(
        "Analyze the resume below and complete ALL steps without asking clarifying questions. "
        "Use these fixed parameters: "
        "Job source = well-known Saudi employers and major job boards (LinkedIn, Bayt). "
        "Location = Riyadh, Saudi Arabia preferred, remote acceptable. "
        "Job type = full-time, entry-level / junior. "
        "Industry focus = AI/ML, NLP, SQL, and data science/Analysis roles. "
        "Cover-letter style = one concise tailored cover letter for the single best match. "
        "Steps: (1) extract skills and experience, (2) list 5-8 matching jobs, "
        "(3) score and rank them, (4) write a cover letter for the top match. "
        "If any detail is missing, make a reasonable assumption and proceed.\n\n"
        f"RESUME:\n{SAMPLE_RESUME}"
    ),
)
print(f"Task ID: {task.id} — waiting (1-3 min)...")
final = local.tasks.wait_for_completion(task.id)
print(f"\nStatus: {final.status}")
print("=" * 60)
print(final.result)
print("=" * 60)


# ─────────────────────────────────────────────
# PHASE 5 — SYNC + PUBLISH  (set DO_SYNC_AND_PUBLISH = True)
# ─────────────────────────────────────────────
if DO_SYNC_AND_PUBLISH:
    print("\nSyncing to cloud...")
    cloud = NavaiaForgeClient(base_url=CLOUD_BASE_URL, api_key=CLOUD_API_KEY)
    result = local.sync.push(wf.id, remote=cloud)
    print(f"Synced — action: {result.action}, cloud ID: {result.workforce_id}")

    cloud.workforces.publish(
        result.workforce_id,
        tagline="Upload a resume, get matched jobs, gap analysis, and a ready-to-send cover letter — 4 AI agents.",
        category="Business Ops",
        price_cents=0,
        currency="SAR",
    )
    print("Published to marketplace — pending moderation.")
    print(f"Cloud workforce ID: {result.workforce_id}")

print(f"\nDONE. Local workforce ID: {wf.id}")
