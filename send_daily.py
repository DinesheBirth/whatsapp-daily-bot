"""
Daily WhatsApp message bot
--------------------------
1. Reads the system prompt + daily prompt from the /prompts folder
2. Asks Gemini to write today's message (same brain as your Gem)
3. Posts it into your WhatsApp group via Whapi.Cloud

Runs automatically once a day on GitHub Actions
(see .github/workflows/daily-whatsapp.yml).

All secrets (API keys, group id) come from environment variables,
so nothing sensitive is ever written inside this code.
"""

import os
import sys
import requests

# ------------------ Settings you can change ------------------
GEMINI_MODEL = "gemini-2.5-flash"   # cheaper option: "gemini-2.5-flash-lite"
USE_GOOGLE_SEARCH = True            # set to False if search ever causes errors
# -------------------------------------------------------------


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def get_message_from_gemini(api_key, system_prompt, daily_prompt):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={api_key}"
    )

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": daily_prompt}]}],
    }

    # This makes Gemini search the internet before answering,
    # exactly like your Gem does. Turn it off above if it ever fails.
    if USE_GOOGLE_SEARCH:
        payload["tools"] = [{"google_search": {}}]

    resp = requests.post(url, json=payload, timeout=60)

    if resp.status_code != 200:
        print("Gemini API error:", resp.status_code)
        print(resp.text)
        sys.exit(1)

    data = resp.json()
    try:
        parts = data["candidates"][0]["content"]["parts"]
        text = "".join(p.get("text", "") for p in parts).strip()
    except (KeyError, IndexError):
        print("Could not read Gemini's response. Full reply below:")
        print(data)
        sys.exit(1)

    if not text:
        print("Gemini returned an empty message.")
        sys.exit(1)

    return text


def post_to_whatsapp(token, group_id, message):
    resp = requests.post(
        "https://gate.whapi.cloud/messages/text",
        headers={"Authorization": f"Bearer {token}"},
        json={"to": group_id, "body": message},
        timeout=60,
    )

    if resp.status_code not in (200, 201):
        print("Whapi error:", resp.status_code)
        print(resp.text)
        sys.exit(1)

    print("Message posted to WhatsApp successfully.")


def main():
    # These come from GitHub Secrets (Step 6 in the guide).
    gemini_key = os.environ["GEMINI_API_KEY"]
    whapi_token = os.environ["WHAPI_TOKEN"]
    group_id = os.environ["WHATSAPP_GROUP_ID"]

    system_prompt = read_file("prompts/system_prompt.txt")
    daily_prompt = read_file("prompts/daily_prompt.txt")

    print("Asking Gemini to write today's message...")
    message = get_message_from_gemini(gemini_key, system_prompt, daily_prompt)

    print("----- Today's message -----")
    print(message)
    print("---------------------------")

    post_to_whatsapp(whapi_token, group_id, message)


if __name__ == "__main__":
    main()
