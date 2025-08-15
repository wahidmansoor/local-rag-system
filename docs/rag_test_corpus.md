---
title: "RAG Test Corpus – Mixed Content"
version: "1.0"
created_utc: "2025-08-15T14:35:51Z"
description: "Single-file, multi-domain dataset for exercising retrieval, chunking, and grounding across formats."
tags: ["RAG", "oncology", "tech-specs", "history", "tables", "logs", "json", "faq"]
---

# RAG Test Corpus – Mixed Content

> Use this file to validate ingestion, chunking, metadata capture, hybrid search (BM25 + embeddings), and grounded generation.

---

## 1) Medical Guideline Excerpt
**Title:** NCCN Guidelines – Breast Cancer (v4.2025) – Summary  
**Category:** Oncology | **Stage:** IIIB

**Recommended Initial Therapy**
- Neoadjuvant chemotherapy: Anthracycline + taxane-based regimen.
- HER2+ disease: Add trastuzumab ± pertuzumab.
- Triple-negative (cT2+ or N+): Consider platinum in neoadjuvant setting.
- Endocrine receptor positive: Endocrine therapy considered in low-proliferation tumors.

**Radiotherapy**
- Post-mastectomy RT for ≥4 positive lymph nodes.
- Consider regional nodal irradiation for high-risk disease.

**Monitoring**
- HER2-directed therapy: Assess LVEF every 3 months.
- CBC/LFTs per protocol; watch for cardiotoxicity and neuropathy.

**Special Populations**
- Avoid anthracyclines if EF < 50% or significant cardiac history.
- Pregnancy: Multidisciplinary review; defer radiation until postpartum.

**Reference:** “NCCN Breast Cancer Guidelines v4.2025”.

---

## 2) Technical Specification Snippet
**System:** OncoVista AI Clinical Decision Support  
- **Backend:** Supabase (PostgreSQL 15)  
- **Frontend:** Next.js 14 + TailwindCSS + shadcn/ui  
- **AI Engine:** GPT-5 + domain-specific embedding model (MiniLM or nomic-embed)  
- **Features:**  
  1. Real-time NCCN/ESMO guideline retrieval  
  2. Interactive oncology calculators  
  3. RAG-powered patient-specific recommendations  
- **Security:** Role-based access control; PHI minimized in logs; audit trails.  
- **Observability:** OpenTelemetry traces; Prometheus metrics; structured JSON logs.  
- **Uptime Goal:** 99.9% SLA

**Key Tables (conceptual)**
```sql
CREATE TABLE public.guidelines (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source text NOT NULL,        -- NCCN | ESMO | ASCO
  version text NOT NULL,       -- e.g., '4.2025'
  cancer_type text NOT NULL,   -- e.g., 'breast'
  stage text,                  -- e.g., 'IIIB'
  content jsonb NOT NULL,
  created_at timestamptz DEFAULT now()
);
```

---

## 3) Historical Event Paragraph
On **July 20, 1969**, Neil Armstrong became the first human to set foot on the Moon during NASA’s Apollo 11 mission. The landing site, known as the **Sea of Tranquility**, was chosen for its flat terrain. Armstrong’s words, “That’s one small step for [a] man, one giant leap for mankind,” were broadcast to an estimated 650 million viewers.

---

## 4) Clinical Case Note
**Patient:** Salim S. N. Alatawi – 61M  
**Diagnosis:** Metastatic urothelial carcinoma, HER2+  
**Key History:** TURBT, bilateral nephrostomy (post-AKI), chemo-radiotherapy; progressed on Enfortumab Vedotin + Pembrolizumab; switched to Trastuzumab Deruxtecan (T-DXd).  
**Imaging:** PET-CT (Jul 2025) – regression in lung and nodal disease; no active bladder lesion.  
**Labs (recent):** Hb 8.2 g/dL, creatinine 210 μmol/L, TSH elevated.  
**Plan:** Continue T-DXd; IR consult for nephrostomy exchange; supportive care (pain control, anemia management).

---

## 5) Table – World Population (Selected Countries, 2025)

| Country       | Population (millions) | Capital  | Official Language |
|---------------|------------------------|----------|-------------------|
| Saudi Arabia  | 36.5                   | Riyadh   | Arabic            |
| Australia     | 26.8                   | Canberra | English           |
| Japan         | 124.2                  | Tokyo    | Japanese          |
| France        | 65.8                   | Paris    | French            |

---

## 6) Software Error Log Example
```
[2025-08-15 10:42:31] ERROR: Uncaught TypeError: Cannot read properties of undefined (reading 'guidelineId')
    at fetchGuidelineData (GuidelinesService.js:42:18)
    at processRequest (server.js:115:22)
    at async handler (api/guidelines.js:20:5)
Supabase Query: SELECT * FROM guidelines WHERE id = NULL
CorrelationId: 7b0a6d0e-1a3e-4bcb-9f64-1a2df0b8f91c
```

**Debugging Tips**
- Validate inputs before DB calls; enforce NOT NULL on `id` filters.
- Prefer parameterized queries; log `CorrelationId` for traceability.
- Add feature flags for demo mode to avoid hitting real tables.

---

## 7) Random Knowledge Snippets
- The chemical symbol for **gold** is **Au** (from Latin *Aurum*).  
- The fastest land animal is the **cheetah** (~112 km/h in short bursts).  
- The **Great Barrier Reef** is the largest coral reef system and is visible from space.

---

## 8) Mini-FAQ (for RAG retrievability)
**Q:** What cardiac monitoring is recommended during HER2 therapy?  
**A:** Assess **LVEF every 3 months**.

**Q:** Which countries in the table have capitals beginning with “C”?  
**A:** **Australia (Canberra)**.

**Q:** What database backs OncoVista AI?  
**A:** **Supabase (PostgreSQL 15)**.

---

## 9) JSON + CSV Examples (semi-structured)

**JSON (guideline record)**
```json
{
  "id": "2b2f9d8c-2e53-4f78-9ed4-1f7b6c2a7e42",
  "source": "NCCN",
  "version": "4.2025",
  "cancer_type": "breast",
  "stage": "IIIB",
  "content": {
    "therapy": ["anthracycline", "taxane", "trastuzumab"],
    "monitoring": {"LVEF_monthly": false, "LVEF_q3mo": true},
    "notes": "Avoid anthracyclines if EF < 50%"
  }
}
```

**CSV (telemetry snapshot)**
```csv
timestamp,service,latency_ms,status,route
2025-08-15T10:41:10Z,api,123,200,/api/guidelines?id=abc
2025-08-15T10:41:11Z,db,18,OK,SELECT_guidelines_by_id
2025-08-15T10:41:12Z,api,502,ERROR,/api/guidelines?id=NULL
```

---

## 10) Short Code Snippet (for code-aware embedding)
```ts
// Defensive fetch with invariant
export async function getGuidelineById(client, id: string) {
  if (!id) throw new Error("guideline id is required");
  const { data, error } = await client
    .from("guidelines")
    .select("*")
    .eq("id", id)
    .single();
  if (error) throw error;
  return data;
}
```

---

## 11) Math / Units
- Creatinine 210 μmol/L ≈ 2.38 mg/dL (conversion: mg/dL = μmol/L ÷ 88.4).  
- EF (ejection fraction) threshold: **50%** for anthracycline caution.

---

## 12) Promptable Assertions (for evaluation)
- *Fact:* Armstrong’s moonwalk date = **1969-07-20**.  
- *Fact:* OncoVista uses **Supabase** and **Next.js 14**.  
- *Fact:* LVEF monitoring during HER2 therapy = **every 3 months**.

---

## 13) Ambiguity Seeds (test disambiguation)
- “Guideline version 4.2025” may refer to **source=‘NCCN’** unless otherwise specified.  
- “EF” in oncology notes usually implies **cardiac ejection fraction**, not **renal** “eGFR”.

---

## 14) Long-ish Paragraph (chunking test)
The implementation of retrieval-augmented generation in clinical decision support requires careful governance of data provenance, auditability, and bias mitigation. Hybrid retrieval that fuses sparse signals (BM25) with dense embeddings reduces false negatives in highly specialized queries. However, chunk sizes must balance token overhead and locality of reference; overly coarse chunks dilute signal, while overly fine chunks inflate recall noise. Domain vocabularies (e.g., *HER2, T-DXd, LVEF*) should be preserved during tokenization to avoid embedding drift. Evaluation should report precision@k, MRR, and context faithfulness, with ablations for query rewriting, rerankers, and caching.

---

### End of File
