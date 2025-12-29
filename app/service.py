import uuid
from rich.console import Console

from .config import settings
from .schemas import AskRequest, AskResponse
from .prompt_manager import load_prompt, render_prompt
from .vector_faiss import search as faiss_search
from .response_formatter import format_context

console = Console()

def answer(req: AskRequest, *, index_dir: str) -> AskResponse:
    correlation_id = str(uuid.uuid4())
    console.print(f"[bold]correlation_id[/bold]={correlation_id} backend={settings.rag_backend} prompt={req.prompt_version}")

    # Retrieval (FAISS local)
    r = faiss_search(index_dir, req.question, top_k=6)
    context, citations = format_context(r, settings.max_context_chars)

    # Prompt governance
    tmpl = load_prompt(req.prompt_version)
    prompt = render_prompt(tmpl, question=req.question, context=context)

    # Local "LLM" fallback for no-AWS demos: echo a grounded answer template.
    # If you set AWS creds and want real inference, wire invoke_bedrock() here.
    answer_text = (
        "Based on the provided context, here is the grounded answer.\n\n"
        "Key points:\n- Review the cited policy sections.\n- If details are missing, respond with uncertainty."
    )

    return AskResponse(
        answer=answer_text,
        used_prompt_version=req.prompt_version,
        citations=citations,
        context_chars=len(context),
    )
