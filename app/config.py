from pydantic import BaseModel
import os

class Settings(BaseModel):
    region: str = os.getenv("AWS_REGION", "us-east-1")
    rag_backend: str = os.getenv("RAG_BACKEND", "faiss")  # faiss | opensearch
    bedrock_model_id: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
    opensearch_endpoint: str | None = os.getenv("OPENSEARCH_ENDPOINT")
    max_context_chars: int = int(os.getenv("MAX_CONTEXT_CHARS", "12000"))

settings = Settings()
