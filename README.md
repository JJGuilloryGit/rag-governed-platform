
# RAG Governed Platform
**Production-Oriented Retrieval-Augmented Generation with Prompt Governance**

This repository demonstrates a **governed RAG (Retrieval-Augmented Generation) platform** designed for **accuracy, reliability, and cost-controlled deployment**.  
It emphasizes **prompt versioning, evaluation, and observability**—the parts required to move GenAI systems from prototype to production.

The demo can be run **locally with no cloud cost**, with an optional path to deploy on **AWS (Bedrock + OpenSearch)**.

---

## What This Demo Shows

- RAG pipeline with embeddings and vector search  
- Prompt versioning and governance  
- Evaluation loop to prevent regressions  
- Cost-aware, production-style architecture  
- Clear separation between ingestion, retrieval, and generation  

This is **not** a notebook demo. It reflects how GenAI systems are engineered in regulated or enterprise environments.

---

## Architecture Overview

1. Documents are ingested and chunked  
2. Embeddings are generated and indexed  
3. Queries retrieve top-K relevant chunks  
4. Prompt templates are versioned and selected  
5. Context is injected into the LLM  
6. Outputs are logged and evaluated  

Execution modes:
- **Local demo mode (FAISS, no AWS)**
- **AWS mode (Bedrock + OpenSearch, optional)**

---

## Repo Structure

```
rag-governed-platform/
├── data/
│   └── sample_docs/
├── prompts/
│   ├── v1.yaml
│   └── v2.yaml
├── src/
│   ├── ingest.py
│   ├── index.py
│   ├── retrieve.py
│   ├── generate.py
│   └── evaluate.py
├── terraform/
├── requirements.txt
└── README.md
```

---

## Quick Start (Local Demo – Recommended)

### 1. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Ingest Demo Documents

```bash
python src/ingest.py
```

### 4. Run a Query

```bash
python src/retrieve.py --query "What does this platform do?"
```

---

## Prompt Governance

Prompts are **versioned artifacts**, not hard-coded strings.

```
prompts/
 ├── v1.yaml
 └── v2.yaml
```

Each version is evaluated before promotion.

---

## Evaluation

```bash
python src/evaluate.py --prompt-version v2
```

Evaluations help prevent silent regressions and enforce quality bars.

---

## Optional AWS Deployment

Components:
- Amazon Bedrock
- OpenSearch
- IAM + Terraform

```bash
cd terraform
terraform init
terraform apply
```

---


---

## License

MIT
