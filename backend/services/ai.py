"""
ai.py — Groq integration (Llama 3.3 70B) for generating professional sales
narrative summaries.
"""
import os
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

_client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])
_MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

_SYSTEM_PROMPT = """You are a senior business analyst at a high-growth company.
Your job is to read raw sales data summaries and write crisp, insightful executive briefs.

Guidelines:
- Write in clear, professional business English — no jargon overload.
- Structure the brief with these sections:
  1. **Executive Summary** (2–3 sentences, the headline insight)
  2. **Key Performance Highlights** (bullet points with specific numbers)
  3. **Regional & Category Breakdown** (patterns across regions / product lines)
  4. **Trends & Observations** (notable changes, outliers, anomalies)
  5. **Recommendations** (2–3 actionable next steps for leadership)
- Use the actual numbers from the data — do not invent figures.
- Keep total length to 350–500 words.
"""


async def generate_summary(data_summary: str) -> str:
    """
    Send the parsed data summary to Groq and return the generated narrative.
    Uses Groq's native async client — no thread-pool wrapper needed.
    """
    chat_completion = await _client.chat.completions.create(
        model=_MODEL_NAME,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Here is the sales data to analyse:\n\n"
                    f"{data_summary}\n\n"
                    "Please write the executive brief now."
                ),
            },
        ],
        temperature=0.4,
        max_tokens=1024,
    )

    return chat_completion.choices[0].message.content.strip()
