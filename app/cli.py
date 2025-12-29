import argparse
from rich.console import Console

from .vector_faiss import build_index
from .schemas import AskRequest
from .service import answer

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Governed RAG CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ingest = sub.add_parser("ingest", help="Build local FAISS index")
    p_ingest.add_argument("--docs", required=True)
    p_ingest.add_argument("--index", required=True)

    p_ask = sub.add_parser("ask", help="Ask a question using RAG")
    p_ask.add_argument("--index", required=True)
    p_ask.add_argument("--prompt-version", default="v1")
    p_ask.add_argument("--question", required=True)

    args = parser.parse_args()

    if args.cmd == "ingest":
        build_index(args.docs, args.index)
        console.print("[green]Index built.[/green]")
        return

    if args.cmd == "ask":
        req = AskRequest(question=args.question, prompt_version=args.prompt_version)
        resp = answer(req, index_dir=args.index)
        console.print("\n[bold]Answer[/bold]")
        console.print(resp.answer)
        console.print("\n[bold]Citations[/bold]")
        for c in resp.citations:
            console.print("-", c, markup=False)
        console.print(f"\n[dim]Context chars used: {resp.context_chars}[/dim]")
        return

if __name__ == "__main__":
    main()
