# Kentucky Dual Credit Chatbot

A Streamlit chatbot that answers questions about Kentucky's Dual Credit program using Claude AI.

## Setup

### 1. Get an Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Go to "API Keys" in the left sidebar
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-...`)

### 2. Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY='your-key-here'

# Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

### 3. Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your GitHub repo and branch
5. Main file path: `app.py`
6. Click "Advanced settings"
7. Add secrets:
   ```
   ANTHROPIC_API_KEY = "your-key-here"
   ```
8. Click "Deploy"

### 4. Embed in WordPress

Add this HTML where you want the chatbot:

```html
<iframe
  src="https://your-app-name.streamlit.app"
  width="100%"
  height="600px"
  frameborder="0">
</iframe>
```

To make it look better, you can add this CSS:

```css
.chatbot-container {
  max-width: 800px;
  margin: 0 auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}
```

## Files

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `dual-credit-research.md` - Knowledge base document
- `README.md` - This file

## Cost

- Streamlit Cloud hosting: **FREE**
- Anthropic API (Claude Sonnet 4): ~$0.003 per question/answer (very cheap)
- Example: 1,000 questions = ~$3

## Model

The chatbot uses **Claude Sonnet 4** (claude-sonnet-4-20250514), the latest model as of December 2025.

## Updating the Knowledge Base

To update the chatbot's knowledge:

1. Edit `dual-credit-research.md`
2. Commit and push to GitHub
3. Streamlit Cloud will auto-redeploy

## Support

For questions about:
- Streamlit: [docs.streamlit.io](https://docs.streamlit.io)
- Anthropic API: [docs.anthropic.com](https://docs.anthropic.com)
