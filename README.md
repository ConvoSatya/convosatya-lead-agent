# ConvoSatya Lead & Opportunity Agent
 
An AI agent that discovers, researches, contacts, and follows up with
startup opportunities using Gemini, Google ADK, and Google Cloud — built
for the **All Things Agentic Hackathon** (Taskmaster category).
 
## The Problem
 
Manually researching investors, accelerators, hackathons, founder events,
and demo nights — then drafting outreach and tracking replies — is slow,
easy to lose track of, and doesn't scale for a team of two. Opportunities
get missed simply because nobody was tracking them in one place.
 
## What It Does
 
This is **one Google ADK agent** with three tools, triggered either on a
schedule or by a loose founder instruction — never by manually entering a
lead. Once triggered, the full cycle runs with no human intervention:
 
- **Discovers** relevant investors, accelerators, hackathons, events, and
  programs using Gemini with search grounding
- **Researches** each one and checks Firestore to avoid duplicates
- **Scores relevance** to ConvoSatya's profile before saving anything
- **Drafts and sends** personalized outreach via Zoho SMTP when a verified
  public email is found — otherwise flags the lead for manual contact
- **Tracks pipeline stage** (Found → Contacted → Replied → Meeting) in
  Firestore
- **Follows up autonomously** on stale leads via a scheduled job — no
  human prompts it
- **Surfaces everything** on a live dashboard
See [SCOPE.md](./SCOPE.md) for the full in-scope / out-of-scope breakdown.
 
## Architecture
 
> Coming soon — system diagram and sequence diagram (Mermaid) will be
> added to [ARCHITECTURE.md](./ARCHITECTURE.md) once the flow is finalized.
 
## Tech Stack
 
| Layer | Choice |
|---|---|
| Agent | Gemini 3.5+ (Flash/Pro) + Google ADK |
| Backend | Python, FastAPI |
| Data | Firestore |
| Async / Scheduling | Cloud Scheduler → Pub/Sub → Cloud Run |
| Frontend | Next.js + Tailwind |
| Hosting | Cloud Run (backend), Firebase Hosting (dashboard) |
| Security | Secret Manager, least-privilege IAM |
| Email | Zoho SMTP |
 
Full breakdown in [Techstack.md](./Techstack.md).
 
## Demo
 
> Coming soon — demo video link and dashboard screenshot/GIF will be added
> before final submission.
 
## Quickstart
 
> Coming soon — setup and run instructions will be added once the backend
> is buildable end-to-end.
 
## Project Structure
 
> Coming soon — will be added once the folder layout is finalized.
 
## Scope
 
v1 focuses on autonomous discovery, research, outreach, and follow-up for
one founder (ConvoSatya). LinkedIn automation is explicitly out of scope
due to ToS risk — the agent only saves a public profile URL for manual
viewing. Full detail in [SCOPE.md](./SCOPE.md).
 
## Security
 
Secrets (Gemini API key, Zoho SMTP credentials) are stored in Secret
Manager, never committed to the repo. The agent runs under a dedicated
service account with least-privilege IAM. Cloud Scheduler authenticates to
Cloud Run via OIDC tokens rather than an open public endpoint.
 
## License
 
MIT — see [LICENSE](./LICENSE).
