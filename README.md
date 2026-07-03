# whatsapp-daily-bot

Sends an AI-generated daily WhatsApp message every morning at 9:30 AM using **Google Gemini** and **Twilio**.

## File structure

```
whatsapp-daily-bot/
├── send_daily.py                  ← main script (Gemini → WhatsApp)
├── requirements.txt               ← Python dependencies
├── README.md                      ← this file
├── .github/workflows/
│   └── daily-whatsapp.yml         ← GitHub Actions cron (9:30 AM daily)
└── prompts/
    ├── system_prompt.txt          ← Gemini system prompt
        └── daily_prompt.txt           ← daily user prompt
        ```

        ## Setup

        ### 1. Clone the repo

        ```bash
        git clone https://github.com/DinesheBirth/whatsapp-daily-bot.git
        cd whatsapp-daily-bot
        ```

        ### 2. Add GitHub Secrets

        Go to **Settings → Secrets and variables → Actions → New repository secret** and add:

        | Secret name | Value |
        |---|---|
        | `GEMINI_API_KEY` | Your Google AI Studio API key |
        | `TWILIO_ACCOUNT_SID` | Your Twilio Account SID |
        | `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
        | `TWILIO_WHATSAPP_FROM` | Twilio sandbox number, e.g. `whatsapp:+14155238886` |
        | `TWILIO_WHATSAPP_TO` | Your WhatsApp number, e.g. `whatsapp:+91XXXXXXXXXX` |

        ### 3. Edit your prompts

        - `prompts/system_prompt.txt` — paste your Gemini system prompt here
        - `prompts/daily_prompt.txt` — paste your daily prompt here (keep it WhatsApp-friendly: plain text, no heavy markdown)

        ### 4. Enable GitHub Actions

        The workflow in `.github/workflows/daily-whatsapp.yml` runs automatically at **9:30 AM UTC** every day.
        You can also trigger it manually from the **Actions** tab → **Run workflow**.

        ## Local test

        ```bash
        pip install -r requirements.txt
        export GEMINI_API_KEY=...
        export TWILIO_ACCOUNT_SID=...
        export TWILIO_AUTH_TOKEN=...
        export TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
        export TWILIO_WHATSAPP_TO=whatsapp:+91XXXXXXXXXX
        python send_daily.py
        ```

        ## Dependencies

        - `google-generativeai` — Gemini SDK
        - `twilio` — WhatsApp messaging via Twilio
