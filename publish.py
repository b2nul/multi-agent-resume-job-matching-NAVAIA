from navaia_forge import NavaiaForgeClient

CLOUD_BASE_URL = "https://fareegi.navaia.sa"
LOCAL_API_KEY = "nf_your_local_key_here"
CLOUD_API_KEY = "nf_your_cloud_key_here"

cloud = NavaiaForgeClient(base_url=CLOUD_BASE_URL, api_key=CLOUD_API_KEY)

# Step 1: set a description on the workforce (required before publishing)
print("Updating description...")
cloud.workforces.update(
    CLOUD_WORKFORCE_ID,
    description=(
        "A 4-agent workforce that analyzes a resume, finds and ranks matching jobs "
        "(Saudi tech market plus remote roles), performs a gap analysis, and writes a "
        "tailored cover letter for the best match. Agents: Resume Analyzer, Job Search, "
        "Matching, and Application Writer, wired as a linear pipeline."
    ),
)
print("Description set.")

# Step 2: publish (no description arg here)
print("Publishing...")
cloud.workforces.publish(
    CLOUD_WORKFORCE_ID,
    tagline="Upload a resume, get matched jobs, gap analysis, and a ready-to-send cover letter — 4 AI agents.",
    category="Business Ops",
    price_cents=0,
    currency="SAR",
)
print("Published! Pending moderation.")
print(f"Cloud workforce ID: {CLOUD_WORKFORCE_ID}")