from google.cloud import firestore

db = firestore.Client(project="convosatya-lead-agent", database="default")

doc_ref = db.collection("leads").document("test_lead_1")
doc_ref.set({
    "name": "Test Investor",
    "category": "investor",
    "stage": "Found",
})

doc = doc_ref.get()
print("Saved document:", doc.to_dict())