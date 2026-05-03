from src.loader    import load_pdf
from src.embedder  import build_index
from src.retriever import retrieve
from src.generator import generate

def main():
    pdf_path = input("PDF path: ").strip()

    chunks = load_pdf(pdf_path)
    index  = build_index(chunks)

    print("\nReady! Type your question (or 'exit' to quit)\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        relevant = retrieve(question, chunks, index)
        answer   = generate(question, relevant)
        print(f"Bot: {answer}\n")

if __name__ == "__main__":
    main()
