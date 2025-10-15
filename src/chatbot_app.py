# src/chatbot_app.py
import os
from typing import List, Dict

from dotenv import load_dotenv
# from mistralai.client import MistralClient
# from mistralai.models.chat_completion import ChatMessage

from dotenv import load_dotenv
from mistralai import Mistral  # ✅ Updated import for new SDK


# Load .env once (MISTRAL_API_KEY, PROVIDER, LLM_MODEL)
load_dotenv()

MODEL = os.getenv("LLM_MODEL", "mistral-large-latest")
print(MODEL)
API_KEY = os.getenv("MISTRAL_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "MISTRAL_API_KEY is not set. Add it to your .env file."
    )

# _client = MistralClient(api_key=API_KEY)

_client = Mistral(api_key=API_KEY)
# creeate a OLLAMA CLIENT,AZURE OPENAI(NEEDS SUBSRIPTION), OPENAI(FREE KEY), HUGGING FACE, AMAZON BEDROCK
# THEN LOAD THE OLLAMA MODEL WHICH IS SIMILAR TO MISTRAL LIST OF  LLM MODELS

# def llm_chat(messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
#     """
#     messages: list of dicts like [{"role":"system","content":"..."},{"role":"user","content":"..."}]
#     returns: assistant string
#     """
#     chat_messages = [ChatMessage(role=m["role"], content=m["content"]) for m in messages]

#     resp = _client.chat(
#         model=MODEL,
#         messages=chat_messages,
#         temperature=temperature,
#     )

def llm_chat(messages, temperature: float = 0.2) -> str:
    resp = _client.chat.complete(
        model=MODEL,
        messages=messages,
        temperature=temperature,
    ) # from mistral documentation, this wikl. ary for different client alwasy
    print(resp)
    # OLD: return resp.output_text
    return resp.choices[0].message.content if resp.choices else ""



        # # Mistral returns choices with .message.content
        # return resp.choices[0].message.content


# Convenience helper tailored for FP&A Q&A
SYSTEM_PROMPT = (
    "You are an FP&A analytics assistant. "
    "Answer ONLY using the numbers and facts provided in the 'Data' section. "
    "If data is insufficient, say what is missing. "
    "Be concise and include the final numeric answer clearly."
    "show your grievance and crack a joke"
)

def ask_fpna_bot(question: str, data_markdown: str) -> str:
    """
    Combines a question and a small, formatted data snippet.
    data_markdown: pre-rendered Snowflake results (small table or bullets)
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Question: {question}\n\nData:\n{data_markdown}"},
    ]
    return llm_chat(messages)


STRUCTURED_SYSTEM_PROMPT = (
    "You are an FP&A analytics assistant.\n"
    "Rules:\n"
    "1) Use ONLY the numbers in the Data section.\n"
    "2) If columns exist named like Month (or Date), Actual (or Actual_Revenue), and Forecast (or Forecast_Revenue), "
    "   calculate Variance = Actual - Forecast and Variance_% = Variance / Forecast.\n"
    "3) Output MUST be:\n"
    "   a) A markdown table with columns: Month | Actual | Forecast | Variance | Variance_%\n"
    "   b) Then a one-line summary: 'Summary: ...'\n"
    "4) If required columns are missing, say exactly which are missing and do NOT guess.\n"
    "5) Use thousands separators for large numbers, and Variance_% with two decimals and a % sign.\n"
)

def ask_fpna_bot_structured(question: str, data_markdown: str) -> str:
    messages = [
        {"role": "system", "content": STRUCTURED_SYSTEM_PROMPT},
        {"role": "user", "content": f"Question: {question}\n\nData:\n{data_markdown}"},
    ]
    return llm_chat(messages, temperature=0.1)
