# Tech Stack — ConvoSatya Lead & Opportunity Agent

## 1. AI / Agent Layer

| Component | Choice | Role |
|---|---|---|
| LLM | Gemini 3.5+ (Flash + Pro split) | Flash for research/search-grounding calls; Pro for relevance scoring and drafting outreach |
| Agent framework | Google ADK (Python) | Wraps the LLM into one agent that decides which tool to call and when |
| Search grounding | Built into Gemini via ADK | Lets the model search the live public web instead of relying on stale training data |
| Agent tools | `discover_and_research()`, `send_outreach_email()`, `log_lead()` / `update_stage()` | All three tools belong to one agent — not separate agents |

## 2. Backend

| Component | Choice | Role |
|---|---|---|
| Language | Python 3.12 | Best ADK / Gemini SDK support |
| Web framework | FastAPI | Receives triggers, invokes the agent, exposes read endpoints for the dashboard |
| Server | Uvicorn (ASGI) | Runs FastAPI inside the container |
| Validation | Pydantic | Type-safe request/response schemas; basic input security |
| SDKs | `google-adk`, `google-genai`, `google-cloud-firestore`, `google-cloud-pubsub`, `google-cloud-secret-manager` | Official Google Cloud client libraries |
| Email sending | `aiosmtplib` | Async SMTP client talking to Zoho's mail servers |

## 3. Data & Database

| Component | Choice | Role |
|---|---|---|
| Database | Firestore (NoSQL, native mode) | No schema migrations, fast to iterate, mandatory-eligible GCP service |
| `leads` collection | name, org, category, stage, relevance_note, sources[], contact_email, email_sent, needs_manual_contact, linkedin_url, created_at, last_updated, follow_up_count | Core pipeline data the dashboard reads |
| `runs` collection | timestamp, trigger type, what was found, actions taken | Audit trail — doubles as proof-of-autonomous-action and basic observability |
| `profile` document | ConvoSatya's industry, stage, location, goals | What autonomous discovery uses to know what to search for |

## 4. Async / Scheduling

| Component | Choice | Role |
|---|---|---|
| Scheduler | Cloud Scheduler | Fires the autonomous discovery cycle and the daily stale-lead follow-up check |
| Message queue | Pub/Sub | Decouples the scheduled trigger from execution; satisfies mandatory infra requirement |
| Compute | Cloud Run | Hosts the FastAPI app; scales to zero when idle |
| Trigger security | Cloud Scheduler → OIDC token → Cloud Run | Scheduler authenticates with a signed token instead of an open endpoint |

## 5. Frontend / Dashboard

| Component | Choice | Role |
|---|---|---|
| Framework | Next.js (React) | Fast to build a board/table view |
| Styling | Tailwind CSS | Fast styling without custom CSS from scratch |
| Data access | Calls FastAPI read endpoints (e.g. `GET /leads`) | Frontend never talks to Firestore directly |
| Hosting | Firebase Hosting (or a second Cloud Run service) | Keeps the whole stack inside Google Cloud |
| View | Stage-grouped board (Found / Contacted / Replied / Meeting) | Makes pipeline motion visually obvious for the demo video |

## 6. Cloud Infrastructure

Cloud Run · Firestore · Pub/Sub · Cloud Scheduler · Secret Manager · Cloud Logging · IAM (service accounts) · Firebase Hosting

## 7. Security

| Layer | Choice |
|---|---|
| Secrets | Secret Manager — Gemini API key, Zoho SMTP app password; never committed to the repo |
| Access control | Dedicated service account, least-privilege IAM (Firestore, Pub/Sub, Secret Manager access only) |
| Endpoint protection | Cloud Scheduler → OIDC auth → Cloud Run; dashboard endpoints behind API key or Firebase Auth |
| Email credentials | Zoho app-specific password, not the real account password |
| Transport | HTTPS by default via Cloud Run |
| Input validation | Pydantic models reject malformed requests before they reach the agent |
| Cost protection | Billing budget alert + Cloud Run max-instance cap |

## 8. DevOps / Deployment

| Component | Choice | Role |
|---|---|---|
| Containerization | Docker | Packages the FastAPI app for Cloud Run |
| Version control | GitHub (ConvoSatya org) | Source of truth, judged directly |
| CI/CD | Cloud Build or GitHub Actions | Either works; Cloud Build keeps it Google-native, GitHub Actions is the more common industry default |

## 9. Testing

| Component | Choice | Role |
|---|---|---|
| Framework | pytest | Unit tests for each tool (research, email, pipeline-logger) with mocked Gemini/Firestore calls |

## 10. Documentation

README.md · ARCHITECTURE.md (with Mermaid diagram) · SCOPE.md · `.env.example` · MIT LICENSE

## Skills This Stack Builds

Agentic tool-calling design · prompt engineering with search grounding ·
async event-driven architecture (Scheduler → Pub/Sub → Cloud Run) · NoSQL
schema design · containerized cloud deployment · IAM least-privilege
thinking · secrets management · full-stack integration (FastAPI ↔ Next.js)
