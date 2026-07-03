# Daily WhatsApp Message Bot

Sends one AI-generated motivational message into your WhatsApp community
every morning at 9:30 AM Sri Lanka time. Free to run (GitHub Actions).

## How it works

1. GitHub Actions wakes up once a day (the cron timer).
2. `send_daily.py` reads your prompts from the `prompts/` folder.
3. It asks the Gemini API to write today's message (same brain as your Gem).
4. It posts the message into your WhatsApp group through Whapi.Cloud.

## Files

| File | What it is |
|------|------------|
| `send_daily.py` | The script that generates + sends the message. |
| `.github/workflows/daily-whatsapp.yml` | The daily timer (runs on GitHub, free). |
| `prompts/system_prompt.txt` | Your Gem's full system prompt (the persona). |
| `prompts/daily_prompt.txt` | Your daily prompt + WhatsApp formatting rules. |
| `requirements.txt` | The one Python package needed. |

## One-time setup

### 1. Get your Gemini API key
- Go to Google AI Studio -> Get API key -> Create API key. Copy it.

### 2. Set up the WhatsApp bridge (Whapi.Cloud)
- Use a SECOND phone number (cheap SIM), not your personal number.
- Make that number an ADMIN of your WhatsApp community/group.
- Sign up at whapi.cloud, open the default channel, scan the QR code
  from that phone: WhatsApp -> Settings -> Linked Devices -> Link a Device.
- Copy your API token.
- Find your group ID (looks like `1203...@g.us`) from their dashboard/API.

### 3. Put these files on GitHub
- Create a new repository (can be private).
- Upload all the files, keeping the same folder structure.

### 4. Paste your prompts (already done for you)
- `prompts/system_prompt.txt` already has your Gem system prompt.
- `prompts/daily_prompt.txt` already has your daily prompt.
- Edit them any time to change the voice.

### 5. Add your secrets in GitHub
Repo -> Settings -> Secrets and variables -> Actions -> New repository secret.
Add these three:
- `GEMINI_API_KEY`
- `WHAPI_TOKEN`
- `WHATSAPP_GROUP_ID`

### 6. Test it
- Go to the Actions tab -> "Daily WhatsApp Message" -> Run workflow.
- Check your WhatsApp group. If the message arrives, you are done.
- It will now run by itself every day at 9:30 AM Sri Lanka time.

## Changing the time
`daily-whatsapp.yml` uses UTC. Sri Lanka is UTC+5:30.
- 9:30 AM SL = `0 4 * * *`
- 7:00 AM SL = `30 1 * * *`
- 6:00 PM SL = `30 12 * * *`

## Safety notes
- Keep it to one message a day. Low volume = low ban risk.
- Never put keys directly in the code. Only use GitHub Secrets.
- If the search step ever errors, open `send_daily.py` and set
  `USE_GOOGLE_SEARCH = False`.
