# InnoVerse AI 2.0 — Caspian SDK Communication Layer Integration

This document describes how `caspian_sdk` is integrated into InnoVerse AI 2.0 to enable communication with the 11 specialist AI agents via **Telegram**, **Discord**, and **Email**.

---

## 🏗️ Architecture Flow

```text
User (Telegram / Discord / Email)
               │
               ▼
       Caspian CommClient (@client.on_message)
               │
               ▼
    integrations.caspian.handlers (CaspianMessageHandler)
               │
               ▼
     backend.caspian.message_router (CaspianMessageRouter)
               │
               ▼
  InnovationDirectorService (Orchestrator) ──► 11 AI Agents (Groq / Gemini)
               │
               ▼
       Caspian message.reply(...)
               │
               ▼
User (Telegram / Discord / Email)
```

---

## ⚙️ Environment Variables

Add the following variables to your [`.env`](file:///c:/Users/ADMIN/Desktop/InnoVerse-AI-2.0/.env) file:

```env
# Caspian Multi-Channel API
CASPIAN_API_KEY=your_caspian_api_key_here
CASPIAN_BASE_URL=https://api.trycaspianai.com

# Bot Credentials
TELEGRAM_BOT_TOKEN=7123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ123456789
DISCORD_BOT_TOKEN=MTUzNjM4MjY4MjI0OTAzNTgxNg...
```

---

## 🤖 Obtaining Bot Tokens

### 1. Telegram Bot Token
1. Open Telegram and search for `@BotFather`.
2. Send `/newbot` and follow the prompts to choose a bot name and username (must end in `bot`).
3. Copy the HTTP API token into `TELEGRAM_BOT_TOKEN`.

### 2. Discord Bot Token
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application**, give it a name, and navigate to **Bot**.
3. Click **Reset Token** to copy your bot token into `DISCORD_BOT_TOKEN`.
4. Enable **Message Content Intent** under Privileged Gateway Intents.

---

## 🚀 How to Run the Integration

### Method 1: Integrated with FastAPI Backend (Recommended)
Start the FastAPI backend, which automatically initializes Caspian and starts the listener:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

### Method 2: Standalone Caspian Service
Run the Caspian service as an independent worker process:

```bash
python -m integrations.caspian.service
```

---

## 🧪 Testing the Integration

Run the unit tests:

```bash
python -m pytest tests/integrations/caspian/ -v
```

---

## 🛡️ Error Handling & Behavior

- **Invalid / Missing Caspian API Key**: The service gracefully disables itself without crashing the FastAPI application.
- **Quota / Account Errors**: Handles `AccountRequiredError`, `InsufficientCreditError`, and `CommError` gracefully, replying with clear warning messages to the user without exposing tokens or internal tracebacks.
