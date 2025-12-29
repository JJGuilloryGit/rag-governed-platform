from .schemas import RetrievalResult

def format_context(r: RetrievalResult, max_chars: int) -> tuple[str, list[str]]:
    parts = []
    cites = []
    total = 0
    for ch in r.chunks:
        tag = f"[source: {ch.doc_id}#{ch.chunk_id}]"
        block = f"{tag}\n{ch.text}\n"
        if total + len(block) > max_chars:
            break
        parts.append(block)
        cites.append(tag)
        total += len(block)
    return "\n".join(parts), cites
