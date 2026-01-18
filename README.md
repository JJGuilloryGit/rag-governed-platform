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


