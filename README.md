RAG Governed Platform

Production-Oriented Retrieval-Augmented Generation with Prompt Governance

This repository demonstrates a governed RAG (Retrieval-Augmented Generation) platform designed for accuracy, reliability, and cost-controlled deployment.
It emphasizes prompt versioning, evaluation, and observability—the parts required to move GenAI systems from prototype to production.

The demo can be run locally with no cloud cost, with an optional path to deploy on AWS (Bedrock + OpenSearch).

What This Demo Shows

✅ RAG pipeline with embeddings + vector search
✅ Prompt versioning and governance
✅ Evaluation loop to prevent regressions
✅ Cost-aware, production-style architecture
✅ Clear separation between ingestion, retrieval, and generation

This is not a notebook demo. It reflects how GenAI systems are engineered in regulated or enterprise environments.

Architecture Overview

High-level flow:

Documents are ingested and chunked

Embeddings are generated and indexed

Queries retrieve top-K relevant chunks

Prompt templates are versioned and selected

Context is injected into the LLM

Outputs are logged and evaluated

Two execution modes are supported:

Local demo mode (FAISS, no AWS)

AWS mode (Bedrock + OpenSearch, optional)

Repo Structure
rag-governed-platform/
│
├── data/
│   └── sample_docs/        # Demo documents for ingestion
│
├── prompts/
│   ├── v1.yaml             # Versioned prompt template
│   └── v2.yaml
│
├── src/
│   ├── ingest.py           # Chunking + embedding pipeline
│   ├── index.py            # Vector index creation
│   ├── retrieve.py         # Retrieval logic (top-K, filters)
│   ├── generate.py         # LLM invocation + context injection
│   └── evaluate.py         # Prompt / output evaluation
│
├── terraform/              # Optional AWS deployment
│
├── requirements.txt
└── README.md

Quick Start (Local Demo – Recommended)

This path runs entirely locally and is ideal for demos, interviews, and experimentation.

1. Create a Virtual Environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

2. Install Dependencies
pip install -r requirements.txt

3. Ingest Demo Documents

This step:

Reads files from data/sample_docs/

Chunks text

Generates embeddings

Builds a FAISS vector index

python src/ingest.py


You should see logs indicating:

Number of chunks created

Index successfully built

4. Run a Query
python src/retrieve.py --query "What does this platform do?"


This will:

Retrieve the most relevant chunks

Apply prompt versioning

Generate a grounded response

Prompt Governance (Key Feature)

Prompts are versioned artifacts, not hard-coded strings.

Example:

prompts/
 ├── v1.yaml
 ├── v2.yaml


Each version can be:

Evaluated

Compared

Promoted or blocked

This prevents silent regressions when prompts change.

Evaluation Workflow

Before promoting a prompt:

python src/evaluate.py --prompt-version v2


Evaluation checks may include:

Groundedness

Retrieval relevance

Output consistency

Regression vs previous version

If evaluation fails, the prompt should not be promoted.

This mirrors real enterprise GenAI governance workflows.

Observability & Production Mindset

Even in demo mode, the platform models production concerns:

Correlation IDs per request

Structured logs

Explicit separation of concerns

Cost-aware retrieval and generation

This is intentional: GenAI systems fail silently unless instrumented.

Optional: AWS Deployment (Advanced)

⚠️ This is optional and not required for the demo.

AWS Components

Amazon Bedrock (LLM inference)

OpenSearch (vector store)

IAM + networking via Terraform

Configure Environment
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=anthropic.claude-v2

Deploy Infrastructure
cd terraform
terraform init
terraform apply


After deployment:

Swap FAISS retrieval for OpenSearch

Switch LLM calls to Bedrock

This allows scaling the same architecture to production.

Why This Project Matters (Interview Framing)

This demo highlights:

RAG correctness over raw generation

Prompt governance as a first-class concern

Evaluation before deployment

Cost-aware design

Production-oriented GenAI engineering

Most GenAI failures are not model failures — they are system design failures.

Who This Is For

AI Engineers

GenAI Engineers

ML Engineers

Cloud / AI Platform Engineers

Especially relevant for roles involving:

Regulated environments

Enterprise AI adoption

Production GenAI systems

Next Steps (Optional Enhancements)

Add LLM-as-Judge scoring

Add UI (Streamlit or FastAPI)

Add request caching

Add human-in-the-loop review

Add CI gate for prompt promotion
