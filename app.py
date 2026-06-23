
import whisper
import gradio as gr
from transformers import pipeline
import os
import csv
from datetime import datetime

# Load all models
print("Loading models...")
whisper_model = whisper.load_model("base")

sentiment_analyzer = pipeline("sentiment-analysis")

intent_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

intents = [
    "refund request", "order tracking",
    "cancel order", "delivery issue",
    "product complaint", "payment issue",
    "wrong item delivered", "general inquiry"
]

print("ALL MODELS READY!")

def save_to_csv(transcript, sentiment, intent, summary):
    file_exists = os.path.exists("calls_log.csv")
    with open("calls_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Transcript",
                           "Sentiment", "Intent", "Summary"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            transcript, sentiment, intent, summary
        ])

def smart_summary(transcript, intent, sentiment):
    sentences = transcript.strip().split(".")
    sentences = [s.strip() for s in sentences if s.strip()]
    keywords = [
        "refund", "order", "arrived", "frustrated",
        "help", "cancel", "delivery", "problem",
        "issue", "want", "need", "complaint",
        "excited", "happy", "angry", "waiting",
        "payment", "wrong", "missing", "damaged"
    ]
    scored = []
    for sentence in sentences:
        score = sum(1 for word in keywords
                   if word in sentence.lower())
        scored.append((score, sentence))
    scored.sort(reverse=True)
    key_sentence = scored[0][1] if scored else sentences[0]
    label = sentiment[0]["label"]
    top_intent = intent["labels"][0]
    summary  = f"Intent     : {top_intent}\n"
    summary += f"Sentiment  : {label}\n"
    summary += f"Key issue  : {key_sentence.strip()}."
    return summary

def analyze_call(audio_file):
    try:
        result = whisper_model.transcribe(audio_file)
        transcript = result["text"]

        sentiment = sentiment_analyzer(transcript[:512])
        label = sentiment[0]["label"]
        score = round(sentiment[0]["score"] * 100)
        sentiment_output = f"{'NEGATIVE — customer is unhappy' if label == 'NEGATIVE' else 'POSITIVE — customer is satisfied'} ({score}% confident)"

        intent = intent_classifier(
            transcript[:512],
            candidate_labels=intents
        )
        intent_output = f"{intent['labels'][0].upper()} ({round(intent['scores'][0] * 100)}% confident)"

        summary = smart_summary(transcript, intent, sentiment)
        save_to_csv(transcript, sentiment_output, intent_output, summary)

        return transcript, sentiment_output, intent_output, summary

    except Exception as e:
        print(f"ERROR: {e}")
        return str(e), str(e), str(e), str(e)

custom_css = """
    .gradio-container {
        font-family: 'Inter', sans-serif !important;
        max-width: 900px !important;
        margin: auto !important;
    }
    .gr-button-primary {
        background: #185FA5 !important;
        border: none !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    .gr-button-primary:hover {
        background: #0C447C !important;
    }
    .gr-textbox {
        border-radius: 8px !important;
        border: 0.5px solid #D3D1C7 !important;
        font-size: 13px !important;
    }
    footer { display: none !important; }
"""

app = gr.Interface(
    fn=analyze_call,
    inputs=gr.Audio(
        sources=["microphone", "upload"],
        type="filepath",
        label="Record or drop customer call recording here"
    ),
    outputs=[
        gr.Textbox(label="Transcript — what the customer said", lines=3),
        gr.Textbox(label="Sentiment — how the customer felt", lines=1),
        gr.Textbox(label="Intent — what the customer wanted", lines=1),
        gr.Textbox(label="Smart summary — call notes for manager", lines=3)
    ],
    title="CallSense — Call Intelligence",
    description="Record live or upload a call recording. AI detects sentiment, intent, and summarizes the issue in seconds.",
    css=custom_css,
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Inter")
    ),
    submit_btn="Analyze call",
    clear_btn="Clear"
)

app.launch()
