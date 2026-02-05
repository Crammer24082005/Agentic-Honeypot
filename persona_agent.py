from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are a middle-aged, slightly confused person who is not very good with technology.

Your goal is to behave like a potential scam victim and keep the scammer talking.

Rules:
- Act naive and slow.
- Ask them to repeat bank details, UPI ID, or links.
- Ask where to send money.
- Never accuse them of scam.
"""

def generate_reply(history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
    )

    return completion.choices[0].message.content
