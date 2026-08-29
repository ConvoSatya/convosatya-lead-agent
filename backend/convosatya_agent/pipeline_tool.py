from google.cloud import firestore

db = firestore.Client(project="convosatya-lead-agent", database="default")


def save_leads(leads: list, sources: list, discovered_via: str, founder_instruction: str = "") -> list:
    """
    Saves researched leads to Firestore, skipping any lead whose name
    already exists. Returns the list of newly saved lead names.
    """
    saved = []
    leads_ref = db.collection("leads")

    for lead in leads:
        name = lead.get("name", "").strip()
        if not name:
            continue

        existing = leads_ref.where("name", "==", name).limit(1).get()
        if len(existing) > 0:
            continue  # already have this lead, skip it

        contact_email = lead.get("contact_email", "").strip() or None

        leads_ref.add({
            "name": name,
            "category": lead.get("category", ""),
            "stage": "Found",
            "relevance_note": lead.get("relevance_note", ""),
            "sources": sources,
            "contact_email": contact_email,
            "email_sent": False,
            "needs_manual_contact": contact_email is None,
            "linkedin_url": lead.get("linkedin_url", "").strip() or None,
            "discovered_via": discovered_via,
            "founder_instruction": founder_instruction,
            "created_at": firestore.SERVER_TIMESTAMP,
            "last_updated": firestore.SERVER_TIMESTAMP,
            "follow_up_count": 0,
        })
        saved.append(name)

    return saved