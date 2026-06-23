# 🎙️ CallSense — Call Intelligence System

An AI-powered call center intelligence system that automatically analyzes customer call recordings and provides instant insights.

## 🌐 Live Demo
👉 [Try CallSense on HuggingFace Spaces](https://huggingface.co/spaces/Prajakta092/callsense)

## 🚀 What it does
Upload or record a customer call → AI instantly provides:
- 📝 **Transcript** — converts speech to text automatically
- 💬 **Sentiment** — detects if customer is happy or angry
- 🎯 **Intent** — identifies what customer wants
- 📋 **Smart Summary** — generates call notes for manager

## 🛠️ Tech Stack
| Tool | Purpose |
|---|---|
| `Whisper` | Speech to text conversion |
| `BERT` | Sentiment analysis |
| `facebook/bart-large-mnli` | Zero shot intent detection |
| `Gradio` | Web UI |
| `gTTS` | Text to speech for testing |

## 💡 Supported Intents
- Refund request
- Order tracking
- Cancel order
- Delivery issue
- Product complaint
- Payment issue
- Wrong item delivered
- General inquiry

## 🏃 How to run locally
```bash
git clone https://github.com/PrajaktaGawade092/callsense
cd callsense
pip install -r requirements.txt
python app.py
```

## 📊 Features
- ✅ Live microphone recording
- ✅ Audio file upload support
- ✅ Auto CSV logging of every call
- ✅ Professional blue UI theme
- ✅ 100% free — no paid APIs

## 🔮 Future upgrades
- Twilio integration for automatic call recording
- Urgency level detection
- Suggested agent reply generation
- Manager dashboard with charts

## 👩‍💻 Built by
Prajakta Gawade — [GitHub](https://github.com/PrajaktaGawade092) · [HuggingFace](https://huggingface.co/Prajakta092)
