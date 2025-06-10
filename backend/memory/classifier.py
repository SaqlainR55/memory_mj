import joblib
import os

# Load paths (adjust if paths differ)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../model/logistic_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, '../model/tfidf_vectorizer.pkl')

# Load model and vectorizer
clf = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# Label mapping
label_map = {
    0: "short-term memory",
    1: "long-term memory",
    2: "short-term memory and long-term memory"
}

def classify_memory_type(prompt: str) -> str:
    """Classifies a prompt into STM, LTM, or both."""
    vec = vectorizer.transform([prompt])
    pred = clf.predict(vec)[0]
    return label_map[pred]
