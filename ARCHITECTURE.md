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

> Coming soon — will show the step-by-step discovery-to-outreach flow
> (matching the 14 steps in SCOPE.md) as a Mermaid sequence diagram, to
> make the "zero human intervention" chain traceable step by step.

## Firestore Schema

> Coming soon — detailed field-level schema for the `leads`, `runs`, and
> `profile` collections.
