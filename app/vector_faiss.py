import os
import json
from pathlib import Path
import numpy as np
import faiss

from .embedding import hash_embed
from .schemas import Chunk, RetrievalResult

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 60) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i:i+chunk_size]
        chunks.append(" ".join(chunk_words))
        i += max(1, chunk_size - overlap)
    return chunks

def build_index(docs_dir: str, out_dir: str) -> None:
    docs_path = Path(docs_dir)
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    all_chunks: list[Chunk] = []
    vectors = []

    for fp in sorted(docs_path.glob("*.txt")):
        raw = fp.read_text(encoding="utf-8")
        doc_id = fp.stem
        chunks = chunk_text(raw)
        for idx, ch in enumerate(chunks):
            all_chunks.append(Chunk(doc_id=doc_id, chunk_id=idx, text=ch))
            vectors.append(hash_embed(ch))

    mat = np.vstack(vectors).astype(np.float32) if vectors else np.zeros((0, 384), dtype=np.float32)
    index = faiss.IndexFlatIP(mat.shape[1] if mat.shape[0] else 384)
    if mat.shape[0]:
        index.add(mat)

    faiss.write_index(index, str(out_path / "index.faiss"))
    (out_path / "chunks.jsonl").write_text(
        "\n".join(c.model_dump_json() for c in all_chunks),
        encoding="utf-8"
    )

def load_index(index_dir: str):
    p = Path(index_dir)
    index = faiss.read_index(str(p / "index.faiss"))
    chunks = []
    for line in (p / "chunks.jsonl").read_text(encoding="utf-8").splitlines():
        chunks.append(Chunk.model_validate_json(line))
    return index, chunks

def search(index_dir: str, query: str, top_k: int = 5) -> RetrievalResult:
    index, chunks = load_index(index_dir)
    q = hash_embed(query).reshape(1, -1)
    scores, ids = index.search(q, top_k)
    out = []
    for i in ids[0]:
        if i == -1:
            continue
        out.append(chunks[int(i)])
    return RetrievalResult(chunks=out)
