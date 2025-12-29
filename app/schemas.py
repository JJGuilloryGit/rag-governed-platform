from pydantic import BaseModel

class Chunk(BaseModel):
    doc_id: str
    chunk_id: int
    text: str

class RetrievalResult(BaseModel):
    chunks: list[Chunk]

class AskRequest(BaseModel):
    question: str
    prompt_version: str = "v1"

class AskResponse(BaseModel):
    answer: str
    used_prompt_version: str
    citations: list[str]
    context_chars: int
