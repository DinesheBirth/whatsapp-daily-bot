import os
import google.generativeai as genai
from twilio.rest import Client

# ── Secrets (set in GitHub → Settings → Secrets) ──────────────────────────────
GEMINI_API_KEY   = os.environ["GEMINI_API_KEY"]
TWILIO_SID       = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_TOKEN     = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_FROM      = os.environ["TWILIO_WHATSAPP_FROM"]   # e.g. whatsapp:+14155238886
TWILIO_TO        = os.environ["TWILIO_WHATSAPP_TO"]     # e.g. whatsapp:+91XXXXXXXXXX

# ── Load prompts ──────────────────────────────────────────────────────────────
with open("prompts/system_prompt.txt", encoding="utf-8") as f:
      system_prompt = f.read().strip()

with open("prompts/daily_prompt.txt", encoding="utf-8") as f:
      daily_prompt = f.read().strip()

# ── Call Gemini ────────────────────────────────────────────────────────────────
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      system_instruction=system_prompt,
)
response = model.generate_content(daily_prompt)
message_text = response.text.strip()

print("=== Gemini response ===")
print(message_text)

# ── Send via Twilio WhatsApp ───────────────────────────────────────────────────
client = Client(TWILIO_SID, TWILIO_TOKEN)
msg = client.messages.create(
      from_=TWILIO_FROM,
      to=TWILIO_TO,
      body=message_text,
)
print(f"Message sent: {msg.sid}")
