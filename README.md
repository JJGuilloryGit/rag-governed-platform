# Production-Grade RAG Platform with Prompt Governance (AWS)

This repo is a reference implementation of a **governed RAG** (Retrieval Augmented Generation)
service on AWS. It demonstrates:

- **RAG grounding** with chunking + embeddings + retrieval
- **Prompt governance** (versioned templates + regression tests)
- **Cost & performance controls** (context pruning, token budgets, caching hooks)
- **Observability-ready logging** (correlation IDs, structured logs)

## Modes
- **Local mode (default)**: FAISS vector index + local docs (no AWS cost)
- **AWS mode (optional)**: Amazon Bedrock + OpenSearch (Terraform scaffold included)

## Quickstart (Local Mode)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Build local index from sample docs
python -m app.cli ingest --docs ./data/sample_docs --index ./data/index

# Ask a question
python -m app.cli ask --index ./data/index --prompt-version v1 --question "What is the refund policy?"
```

## Quickstart (AWS Mode)
1. Configure AWS credentials.
2. Deploy infra (optional):
```bash
cd terraform
terraform init
terraform apply
```
3. Set env vars:
- `AWS_REGION`
- `BEDROCK_MODEL_ID` (e.g., an available Bedrock text model in your region)
- `RAG_BACKEND=opensearch`
- `OPENSEARCH_ENDPOINT=...`

- flowchart TB
  %% =========================
  %% Actors / Entry Points
  %% =========================
  U[User / Client] -->|Question| Q[Query API / CLI: ask]

  %% =========================
  %% Prompt Governance
  %% =========================
  subgraph PG[Prompt Governance]
    PV[Select prompt version (e.g., v1)]
    PT[Prompt template library (versioned)]
    RG[Regression tests against prompts]
  end

  Q --> PV --> PT

  %% =========================
  %% Retrieval Backends (Local vs AWS)
  %% =========================
  subgraph ING[Ingestion / Index Build]
    D[Docs: ./data/sample_docs]
    CH[Chunking]
    EM[Embeddings]
    IDX[Build / Update Index]
  end

  subgraph RB[Retrieval Backend]
    direction TB
    L1[Local Mode: FAISS index\n(no AWS cost)]
    A1[AWS Mode: OpenSearch\n(optional Terraform scaffold)]
  end

  %% Ingest path
  D --> CH --> EM --> IDX
  IDX --> L1
  IDX --> A1

  %% Query -> Retrieve path
  Q -->|Retrieve| RET[Retriever: top-k + metadata filtering]
  RET -->|Local| L1
  RET -->|AWS| A1

  %% =========================
  %% Cost/Perf Controls + Generation
  %% =========================
  subgraph GEN[Generation]
    CP[Context pruning / token budgets / caching hooks]
    CTX[Assemble grounded context]
    LLM[LLM / Model\nLocal stub OR Amazon Bedrock]
    ANS[Answer + citations/grounding]
  end

  L1 --> RET
  A1 --> RET
  RET --> CP --> CTX --> LLM --> ANS

  %% =========================
  %% Observability
  %% =========================
  subgraph OBS[Observability]
    CID[Correlation IDs]
    LOG[Structured logs]
    MET[Metrics/Tracing hooks]
  end

  Q --> CID --> LOG --> MET
  ANS --> LOG

  %% =========================
  %% Evaluation Loop
  %% =========================
  subgraph EVAL[Evaluation & Governance Loop]
    EV[Evaluation suite]
    FAIL[Fail build / block prompt promotion]
    PASS[Promote prompt version]
  end

  RG --> EV
  EV -->|issues| FAIL
  EV -->|meets quality bar| PASS
  PASS --> PV



