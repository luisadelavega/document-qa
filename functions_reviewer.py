import requests
from bs4 import BeautifulSoup
import os
from openai import OpenAI
import streamlit as st


# ------------------------------------------------------------
# 1. Scrape full visible text from a URL
# ------------------------------------------------------------
def scrape_full_text(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0 Safari/537.36"
        )
    }

    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    return soup.get_text(separator="\n", strip=True)

# ------------------------------------------------------------
# 2. Analyze language + detect errors with the LLM
# ------------------------------------------------------------
def analyze_language_and_errors(full_text: str) -> str:
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    # max_chars = 20000
    # if len(full_text) > max_chars:
    #     full_text = full_text[:max_chars]

    system_msg = (
        "You are a professional linguist and native-level copy editor.\n"
        "Your tasks:\n"
        "1. Identify all languages present and decide which is the majority language.\n"
        "2. Find words from foreign languages (unless proper nouns) or unnatural/wrong phrases.\n"
        "3. Split each issue into:\n"
        "   (1) Critical errors to fix. For example, a sentence or word in a different language.\n"
        "   (2) Light errors. For example, a term that is not very common for a native speaker.\n"
        "4. For each issue: provide the original snippet, corrected suggestion, and explanation.\n"
        "Respond in markdown with:\n"
        "Language detection:\n"
        "- Main language: ...\n"
        "- Other languages: ...\n\n"
        "1) Critical errors to fix:\n"
        "- ...\n\n"
        "2) Light errors:\n"
        "- ..."
    )

    user_msg = (
        "Analyze the following raw web page text.\n\n"
        "=== PAGE TEXT BEGIN ===\n"
        f"{full_text}\n"
        "=== PAGE TEXT END ==="
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content
