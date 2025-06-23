from transformers import pipeline

# Load once (reuse this across transcripts)
summarizer = pipeline("summarization", model="t5-small")  # Or try "facebook/bart-base"

def generate_title(transcript, max_words=20):
    if not transcript.strip():
        return "No transcript"

    result = summarizer(transcript, max_length=max_words, min_length=5, do_sample=False)
    return result[0]['summary_text']

