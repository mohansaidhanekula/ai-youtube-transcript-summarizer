# AI YouTube Transcript Summarizer
# Fetches YouTube transcripts and generates summaries, key points, and chapter timestamps

from youtube_transcript_api import YouTubeTranscriptApi
import openai
import re
from datetime import datetime

openai.api_key = "YOUR_OPENAI_API_KEY"

# ============================================================
# 1. VIDEO ID EXTRACTOR
# ============================================================
def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    patterns = [
        r'v=([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'embed/([a-zA-Z0-9_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url  # Assume URL is already a video ID


# ============================================================
# 2. TRANSCRIPT FETCHER
# ============================================================
def get_transcript(video_id: str, language: str = 'en') -> dict:
    """Fetch transcript for a YouTube video."""
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        full_text = ' '.join([entry['text'] for entry in transcript_data])
        duration = transcript_data[-1]['start'] + transcript_data[-1]['duration'] if transcript_data else 0
        return {
            "success": True,
            "text": full_text,
            "segments": transcript_data,
            "duration_seconds": int(duration),
            "word_count": len(full_text.split()),
            "segment_count": len(transcript_data)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
# 3. AI SUMMARIZER
# ============================================================
def summarize_transcript(transcript_text: str, summary_type: str = "bullet") -> dict:
    """Generate different types of summaries from transcript."""
    # Truncate to API limit
    text = transcript_text[:8000]

    prompts = {
        "bullet": "Summarize this YouTube video transcript into 5-7 key bullet points. Be concise and informative.",
        "paragraph": "Write a 2-3 paragraph summary of this YouTube video transcript.",
        "tldr": "Give a one-sentence TLDR summary of this video.",
        "chapters": "Identify 4-6 main topics/chapters in this transcript with approximate timestamps."
    }

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a video content analyst. Create clear, structured summaries."},
            {"role": "user", "content": f"{prompts[summary_type]}\n\nTranscript:\n{text}"}
        ]
    )
    return {"summary_type": summary_type, "content": response.choices[0].message.content}


# ============================================================
# DEMO OUTPUT (Simulated - sample ML video)
# ============================================================
if __name__ == "__main__":
    print("AI YOUTUBE TRANSCRIPT SUMMARIZER")
    print("=" * 60)
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Simulated output for a Machine Learning tutorial video
    DEMO_VIDEOS = [
        {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "title": "Complete Machine Learning Course - Beginner to Advanced",
            "duration": "2:34:18",
            "duration_seconds": 9258,
            "word_count": 18420,
            "segment_count": 1843,

            "tldr": "A comprehensive guide covering ML fundamentals from linear regression to deep learning, with Python code examples and real-world projects.",

            "bullet_summary": [
                "Introduction to Machine Learning concepts: supervised, unsupervised, and reinforcement learning paradigms",
                "Data preprocessing techniques: handling missing values, normalization, feature engineering, and train-test splitting",
                "Classical algorithms covered: Linear Regression, Logistic Regression, Decision Trees, Random Forest, SVM, and KNN",
                "Deep Learning section: Neural Networks, CNNs for image classification, RNNs and LSTMs for sequence modeling",
                "Hands-on Python projects: Iris classification, House price prediction, Sentiment analysis, and Image recognition",
                "Model evaluation metrics: Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Cross-validation strategies",
                "Deployment basics: saving models with pickle/joblib, creating REST APIs with Flask/FastAPI"
            ],

            "chapters": [
                {"time": "0:00", "topic": "Introduction to Machine Learning"},
                {"time": "18:32", "topic": "Data Preprocessing and EDA"},
                {"time": "45:14", "topic": "Classical ML Algorithms"},
                {"time": "1:22:08", "topic": "Introduction to Deep Learning"},
                {"time": "1:58:33", "topic": "Hands-on Projects"},
                {"time": "2:20:15", "topic": "Model Deployment"}
            ]
        }
    ]

    for video in DEMO_VIDEOS:
        print(f"\nVIDEO: {video['title']}")
        print(f"URL  : {video['url']}")
        print(f"Duration   : {video['duration']} ({video['duration_seconds']} seconds)")
        print(f"Word Count : {video['word_count']:,} words")
        print(f"Segments   : {video['segment_count']}")

        print(f"\n[TLDR]")
        print(f"  {video['tldr']}")

        print(f"\n[KEY POINTS]")
        for i, point in enumerate(video['bullet_summary'], 1):
            print(f"  {i}. {point}")

        print(f"\n[VIDEO CHAPTERS]")
        for ch in video['chapters']:
            print(f"  {ch['time']:>8}  |  {ch['topic']}")

    print(f"\n{'='*60}")
    print("PROCESSING STATS")
    for v in DEMO_VIDEOS:
        print(f"  Video      : {v['title'][:50]}...")
        print(f"  Summary    : {len(v['bullet_summary'])} bullet points")
        print(f"  Chapters   : {len(v['chapters'])} sections identified")
        compression = (1 - 100/v['word_count']) * 100
        print(f"  Compression: {compression:.1f}% reduction")
    print(f"{'='*60}")
