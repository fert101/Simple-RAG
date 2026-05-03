from groq import Groq
from src.config import GROQ_API_KEY, CHAT_MODEL

client = Groq(api_key=GROQ_API_KEY)

def generate(question: str, chunks: list[str]) -> str:
    context  = "\n\n".join(chunks)
    response = client.chat.completions.create(
        model    = CHAT_MODEL,
        messages = [
            {
                "role"   : "system",
                "content": (
                    "Answer only using the context below. "
                    "If the answer isn't there say 'Not found in document.'"
                    f"\n\nContext:\n{context}"
                )
            },
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content