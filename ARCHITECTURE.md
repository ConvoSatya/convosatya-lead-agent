# Architecture — ConvoSatya Lead & Opportunity Agent

This document describes the system architecture for the ConvoSatya Lead &
Opportunity Agent. See [SCOPE.md](./SCOPE.md) for the full functional flow
and [Techstack.md](./Techstack.md) for the complete technology breakdown.

## System Architecture

One Google ADK agent, three tools, triggered either by a schedule or a
loose founder instruction — never by manually creating a lead.

```mermaid
flowchart TD
    subgraph TRIG["Triggers"]
        T1["Cloud Scheduler — Autonomous Discovery"]
        T2["Founder Input — Dashboard"]
    end

    subgraph CORE["Agent Core — Cloud Run"]
        C1["FastAPI"]
        C2["Google ADK Agent"]
    end

    subgraph TOOLS["Agent Tools — one agent, three tools"]
        TL1["Discovery & Research Tool"]
        TL2["Outreach Email Tool"]
        TL3["Pipeline Logger Tool"]
    end

    subgraph EXT["External Services"]
        E1["Gemini — Search Grounding"]
        E2["Zoho SMTP"]
    end

    subgraph DATA["Data — Firestore"]
        D1[("leads / runs / profile")]
    end

    subgraph ASYNC["Autonomous Follow-up Loop"]
        A1["Cloud Scheduler — Daily"]
        A2["Pub/Sub"]
        A3["Cloud Run — Follow-up Worker"]
    end

    subgraph FE["Frontend"]
        F1["Next.js Dashboard — Firebase Hosting"]
    end

    subgraph SEC["Security"]
        S1["Secret Manager"]
        S2["IAM Service Account"]
    end

    T1 --> C1
    T2 --> C1
    C1 --> C2
    C2 --> TL1
    C2 --> TL2
    C2 --> TL3
    TL1 --> E1
    TL2 --> E2
    TL1 --> D1
    TL2 --> D1
    TL3 --> D1
    D1 --> F1
    A1 --> A2 --> A3
    A3 --> D1
    A3 --> C2
    S1 -.-> CORE
    S1 -.-> A3
    S2 -.-> CORE
```

**How to read this:**

- **Triggers** — both entry points (the clock, or the founder) land on the
  same FastAPI endpoint.
- **Agent Core** — FastAPI receives the request and hands it to a single
  ADK agent. There is no multi-agent orchestration in this system.
- **Agent Tools** — three tools belonging to that one agent, not separate
  agents: Discovery & Research, Outreach Email, and Pipeline Logger.
- **External Services** — Gemini (search grounding) and Zoho SMTP are
  called by the tools but are not part of ConvoSatya's own infrastructure.
- **Data** — Firestore is the single source of truth. All three tools
  write to it; the dashboard only ever reads from it.
- **Autonomous Follow-up Loop** — runs on its own schedule, independent of
  any human action, and loops back into the same agent core days later.
  This is the core proof of "no human intervention."
- **Security** — dotted lines indicate a permissions relationship, not
  data flow: Secret Manager and IAM apply underneath the Agent Core and
  the Follow-up Worker.

## Sequence Diagram

This shows one full discovery-to-outreach cycle, step by step. The same
component names from the System Architecture diagram are reused here for
consistency.

```mermaid
sequenceDiagram
    actor Trigger as Trigger (Scheduler / Founder)
    participant API as FastAPI
    participant Agent as ADK Agent
    participant RT as Research Tool
    participant Gemini
    participant DB as Firestore
    participant ET as Email Tool
    participant Zoho as Zoho SMTP
    participant Dash as Dashboard

    Trigger->>API: Start discovery cycle
    API->>Agent: Forward request
    Agent->>RT: discover_and_research()
    RT->>Gemini: Search grounding query
    Gemini-->>RT: Candidates (people/orgs/events)
    RT->>DB: Check for duplicate leads
    DB-->>RT: Existing lead list
    RT->>Gemini: Score relevance
    Gemini-->>RT: Relevance score + notes
    RT->>DB: Save lead (stage = Found)
    Agent->>ET: Draft outreach from research

    alt Verified public email found
        ET->>Zoho: Send outreach email
        Zoho-->>ET: Sent confirmation
        ET->>DB: Update stage Found -> Contacted
    else No verified email found
        ET->>DB: Flag needs_manual_contact = true
    end

    DB-->>Dash: Reflects updated lead on next read

    note over Trigger,Dash: Days later, Cloud Scheduler fires the Follow-up Worker on stale "Contacted" leads, re-entering this same Agent to Email Tool to Firestore path with zero human input.
```

**Why this diagram matters for judging:** there is no participant in this
chain representing a human approving a step. The `Trigger` actor only
*starts* the cycle — every arrow after that is agent-to-tool or
tool-to-service. The closing note is the visual proof that the follow-up
loop re-enters this exact same path autonomously, days later.

## Firestore Schema

Three collections. `leads` and `runs` grow over time; `profile` is a
single document describing ConvoSatya itself.

### `leads` — one document per opportunity

| Field | Type | Purpose |
|---|---|---|
| `name` | string | Who or what this lead is |
| `category` | string | investor / accelerator / hackathon / event / demo_night / startup_program |
| `stage` | string | Found -> Contacted -> Replied -> Meeting |
| `relevance_note` | string | Gemini's reasoning for why this is a good match |
| `sources` | array\<string\> | URLs used during research (credibility / audit trail) |
| `contact_email` | string \| null | Email found, if any |
| `email_sent` | boolean | Whether outreach actually went out |
| `needs_manual_contact` | boolean | True when no verified email was found |
| `linkedin_url` | string \| null | View-only, never automated |
| `discovered_via` | string | "autonomous" or "founder_guided" |
| `founder_instruction` | string \| null | The founder's original instruction, if guided |
| `created_at` | timestamp | When first found |
| `last_updated` | timestamp | Last change to this lead |
| `follow_up_count` | number | How many autonomous follow-ups have fired |

### `runs` — one document per agent execution (audit trail)

| Field | Type | Purpose |
|---|---|---|
| `trigger_type` | string | scheduled_discovery / founder_guided / scheduled_followup |
| `started_at` | timestamp | Run start |
| `completed_at` | timestamp | Run end |
| `leads_found` | number | New leads produced this run |
| `leads_contacted` | number | Emails sent this run |
| `summary` | string | Short human-readable description of what happened |

### `profile` — single document describing ConvoSatya

| Field | Type | Purpose |
|---|---|---|
| `industry` | string | Used to bias autonomous discovery |
| `stage` | string | Startup stage, e.g. "pre-seed" |
| `location` | string \| array | Geographic focus |
| `goals` | array\<string\> | What kinds of opportunities to look for |
| `keywords` | array\<string\> | Search terms for autonomous runs |

**Note:** `stage`, `category`, and `discovered_via` are plain strings, not
enums — Firestore has no enum type. Allowed values are enforced in the
FastAPI/Pydantic layer, not the database itself.
