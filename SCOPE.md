# Project Scope — ConvoSatya Lead & Opportunity Agent

**Hackathon:** All Things Agentic Hackathon (Devpost)
**Category:** Taskmaster
**Organization:** ConvoSatya LLC

## Problem

Manually researching investors, accelerators, hackathons, founder events, and
demo nights — then drafting outreach and tracking replies — is slow, easy to
lose track of, and doesn't scale for a solo founder. Opportunities get missed
simply because nobody was tracking them in one place.

## What the Agent Does

This is **one Google ADK agent** with three tools it can call: Discovery &
Research, Outreach Email, and Pipeline Logging. It is not a multi-agent
system — a single agent orchestrates all three capabilities.

The founder never manually creates a lead record. Discovery is always
performed by the agent itself, triggered one of two ways:

### 1. Autonomous discovery
A scheduled job (Cloud Scheduler) asks the agent to search for relevant:
- Investors
- Accelerators
- Hackathons
- Founder events
- Demo nights
- Startup programs

The search is based on ConvoSatya's stored profile — industry, location,
startup stage, and goals.

### 2. Founder-guided discovery
The founder may optionally give a loose natural-language instruction, e.g.:
- "Find AI investors in New York"
- "Find startup events happening in Connecticut"
- "Research Sarah Guo"
- "Research the Antler accelerator"

The founder provides only a name, category, or search instruction — the
agent is responsible for finding and organizing everything else.

## v1 — In Scope: Discovery & Research Flow

1. Cloud Scheduler or the founder starts a discovery request.
2. The FastAPI backend sends the request to the Google ADK agent.
3. The agent calls its Discovery & Research tool.
4. Gemini, with search grounding, searches permitted public web sources.
5. The tool finds relevant people, organizations, programs, or events.
6. It extracts publicly available professional information.
7. It checks Firestore to avoid duplicate leads.
8. Gemini evaluates how relevant each opportunity is to ConvoSatya.
9. Relevant opportunities are saved to Firestore at stage **Found**.
10. The agent prepares personalized outreach using the research.
11. **If** a verified public business email is found, Zoho SMTP sends the
    outreach email and the stage moves **Found → Contacted**.
12. **If no verified public email is found**, the lead stays at stage
    **Found** and is flagged `needs_manual_contact: true` so it's clearly
    visible on the dashboard. The founder locates the contact manually
    through another source — the agent does not block or retry endlessly.
13. A scheduled follow-up job checks stale "Contacted" leads and
    autonomously sends a follow-up if there's been no reply — this is the
    core "runs without human intervention" proof for judging.
14. The dashboard displays every opportunity: research, sources, stage,
    email status, and history — one place to see everything.

## v1 — In Scope: Dashboard

- Single stage-grouped board view: **Found → Contacted → Replied → Meeting**
- Each lead card shows: name/org, category, relevance note, sources,
  email-sent status (or "needs manual contact" flag), LinkedIn URL (if
  found), last updated, follow-up count
- Read-only, plus one manual "mark as contacted" action
- Reads from FastAPI endpoints — never talks to Firestore directly

## v1 — Explicitly Out of Scope (Future Work)

- **LinkedIn automation** — no scraping, no automated DMs. A public LinkedIn
  profile URL may be saved for the founder to view and message manually.
  This is a deliberate exclusion due to LinkedIn ToS risk.
- Multi-agent sub-agent orchestration (this is one agent, multiple tools).
- Vector search / RAG over historical leads.
- Dashboard filtering, search, analytics/charts, or manual lead creation
  from the UI.

## Success Criteria

- A full discovery cycle (find → research → score → draft → send/flag →
  log) completes with zero manual intervention after the initial trigger.
- The follow-up job demonstrably fires on a schedule, without a human
  prompting it, and is visible in the demo video.
- The dashboard shows the pipeline moving across stages in real time.
