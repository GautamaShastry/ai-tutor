# API Keys Setup Guide

This guide helps you set up the necessary API keys for the Telugu AI Tutor.

## Required vs Optional Keys

### ✅ Required (for chat features to work)
- **Gemini API Key** OR **Ollama** (local)

### 🔧 Optional (for better features)
- **OpenAI API Key** (for better embeddings)

---

## 1. Gemini API Key (Recommended - FREE)

Gemini is Google's LLM with excellent Telugu support and a generous free tier.

### Get Your Free Gemini API Key:

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### Add to .env file:

```bash
# Edit backend/.env
GEMINI_API_KEY=your-actual-key-here
LLM_PROVIDER=gemini
```

### Free Tier Limits:
- 60 requests per minute
- 1,500 requests per day
- Perfect for development and small-scale use

---

## 2. Ollama (Alternative - FREE, Local)

Run LLMs locally on your machine. No API key needed!

### Install Ollama:

1. Download from: https://ollama.ai
2. Install for your OS
3. Open terminal and run:
   ```bash
   ollama pull llama3.2
   # or for better Telugu support:
   ollama pull qwen2.5
   ```

### Configure in .env:

```bash
# Edit backend/.env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

### Pros:
- ✅ Free
- ✅ Private (runs locally)
- ✅ No rate limits

### Cons:
- ❌ Requires ~4GB RAM
- ❌ Slower than cloud APIs
- ❌ Telugu support varies by model

---

## 3. OpenAI API Key (Optional)

Only needed if you want to re-ingest data with better embeddings.

### Get OpenAI API Key:

1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key

### Add to .env:

```bash
# Edit backend/.env
OPENAI_API_KEY=your-actual-key-here
```

### Cost:
- Embeddings: ~$0.02 per 1,000 items
- For 5,000 items: ~$0.10
- Chat completions: ~$0.002 per request

### When to use:
- If you want semantic search to work properly
- If dummy embeddings aren't sufficient
- For production deployment

---

## Quick Setup Steps

### Option A: Using Gemini (Easiest)

```bash
# 1. Get Gemini API key from: https://makersuite.google.com/app/apikey

# 2. Edit backend/.env
nano backend/.env  # or use any text editor

# 3. Add your key:
GEMINI_API_KEY=your-key-here
LLM_PROVIDER=gemini

# 4. Save and restart backend
```

### Option B: Using Ollama (Free, Local)

```bash
# 1. Install Ollama from: https://ollama.ai

# 2. Pull a model
ollama pull llama3.2

# 3. Edit backend/.env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434

# 4. Start Ollama (it runs automatically after install)

# 5. Restart backend
```

---

## Verify Setup

### Test Gemini:

```bash
cd backend
python -c "
import os
from google import generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content('Say hello in Telugu')
print(response.text)
"
```

Should output: "నమస్కారం" or similar Telugu greeting

### Test Ollama:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Say hello in Telugu",
  "stream": false
}'
```

---

## Security Best Practices

### 1. Never Commit API Keys

The `.env` file is already in `.gitignore`. Always use `.env.example` for templates.

### 2. Rotate Keys Regularly

Change your API keys every few months, especially if:
- You suspect they've been exposed
- Team members leave
- Moving to production

### 3. Use Environment-Specific Keys

```bash
# Development
GEMINI_API_KEY=dev-key-here

# Production (separate key)
GEMINI_API_KEY=prod-key-here
```

### 4. Monitor Usage

- Check Gemini usage: https://makersuite.google.com/app/apikey
- Check OpenAI usage: https://platform.openai.com/usage

---

## Troubleshooting

### "Invalid API key" error

**Gemini:**
- Verify key at: https://makersuite.google.com/app/apikey
- Check for extra spaces in `.env` file
- Ensure no quotes around the key

**OpenAI:**
- Verify key at: https://platform.openai.com/api-keys
- Check if key has been revoked
- Ensure billing is set up

### "Connection refused" with Ollama

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

### Rate limit errors

**Gemini:**
- Free tier: 60 requests/minute
- Wait a minute and try again
- Or upgrade to paid tier

**OpenAI:**
- Check your usage limits
- Add billing information
- Upgrade your plan

---

## Cost Estimation

### For 1,000 Users/Month:

**Using Gemini (Free Tier):**
- Cost: $0
- Limits: May hit rate limits with heavy usage

**Using Gemini (Paid):**
- ~10,000 requests/month
- Cost: ~$5-10/month

**Using Ollama:**
- Cost: $0 (just server costs)
- Server: ~$20-50/month for VPS

**Using OpenAI:**
- ~10,000 requests/month
- Cost: ~$20-30/month

---

## Recommended Setup

### For Development:
```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-free-key
# No OpenAI key needed
```

### For Production (Small Scale):
```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-paid-key
OPENAI_API_KEY=your-key  # Optional
```

### For Production (Large Scale):
```bash
LLM_PROVIDER=ollama  # Self-hosted
OLLAMA_BASE_URL=http://your-server:11434
OPENAI_API_KEY=your-key  # For embeddings
```

---

## Next Steps

1. ✅ Choose your LLM provider (Gemini or Ollama)
2. ✅ Get API key or install Ollama
3. ✅ Update `backend/.env` file
4. ✅ Restart the backend server
5. ✅ Test chat features in the app

Need help? Check the troubleshooting section or refer to `PROJECT_READY.md`.
