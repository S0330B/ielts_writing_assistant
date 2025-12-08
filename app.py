import streamlit as st
from dotenv import load_dotenv
from groq_client import groq_generate
import requests

load_dotenv()
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

st.set_page_config(
    page_title="IELTS Writing Task Generator (Band 9)",
    page_icon="✍️",
    layout="wide"
)

st.title("✍️ IELTS Writing Task Generator – Band 9")
st.caption("Generate context-based vocabulary, grammar structures, and a Band-9 level essay.")

# ------------------ FUNCTIONS ------------------ #

def generate_ielts_content(topic: str) -> dict:
    vocabulary_prompt = f"""
    You are an IELTS examiner.
    Generate 25–30 high-level IELTS vocabulary words related to this topic.
    Provide them comma-separated without explanation.

    Topic: {topic}
    """

    grammar_prompt = f"""
    You are an IELTS grammar expert.
    Generate 12–15 advanced IELTS grammar structures suitable for Band 8–9 candidates.
    Provide them as short phrases, comma-separated.

    Topic: {topic}
    """

    essay_prompt = f"""
    You are an official IELTS examiner.
    Write a full Band-9 IELTS Writing Task 2 essay with exactly 4 paragraphs (Introduction, Body 1, Body 2, Conclusion).
    
    ✅ Formal academic tone  
    ✅ Clear introduction, body paragraphs, and conclusion  
    ✅ Advanced vocabulary and grammar  
    ✅ Coherent arguments and examples  
    ✅ Paragraphs separated clearly

    Topic:
    {topic}
    """

    return {
        "vocabulary": groq_generate(vocabulary_prompt),
        "grammar": groq_generate(grammar_prompt),
        "essay": groq_generate(essay_prompt),
    }


def clean_list(text: str):
    if ":" in text:
        text = text.split(":", 1)[1]
    return [item.strip().capitalize() for item in text.split(",") if item.strip()]

def get_word_meaning(word: str):
    """Use Free Dictionary API"""
    if not word:
        return ""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
        return meaning
    except Exception:
        return "Meaning not found."

# ------------------ SESSION STATE ------------------ #
if "generated" not in st.session_state:
    st.session_state.generated = False
if "vocab" not in st.session_state:
    st.session_state.vocab = []
if "grammar" not in st.session_state:
    st.session_state.grammar = []
if "essay" not in st.session_state:
    st.session_state.essay = ""
if "meaning" not in st.session_state:
    st.session_state.meaning = ""

# ------------------ UI ------------------ #

# --- Topic Input ---
topic = st.text_area(
    "📌 Enter IELTS Writing Task Topic",
    placeholder="Some people believe that technology has made our lives more complicated. Discuss both views and give your opinion.",
    height=120
)

# --- Search Box (Persistent) ---
col_main, col_search = st.columns([3, 1])
with col_search:
    search_word = st.text_input("🔍 Search Word")
    if st.button("Search Meaning"):
        if search_word.strip():
            st.session_state.meaning = get_word_meaning(search_word.strip())

# --- Display meaning ---
if st.session_state.meaning:
    st.info(f"**{search_word.strip()}**: {st.session_state.meaning}")

# --- Generate Button ---
with col_main:
    generate = st.button("🎯 Generate Band-9 Content", type="primary")

# --- Generate Content ---
if generate:
    if not topic.strip():
        st.error("Please enter an IELTS writing task topic.")
    else:
        with st.spinner("Generating Band-9 IELTS content..."):
            raw = generate_ielts_content(topic)

        st.session_state.vocab = clean_list(raw["vocabulary"])
        st.session_state.grammar = clean_list(raw["grammar"])
        st.session_state.essay = raw["essay"]
        st.session_state.generated = True
        st.success("✅ Band-9 Content Generated")

# --- Display Vocabulary & Grammar ---
if st.session_state.generated:
    col_vocab, col_grammar = st.columns(2)

    with col_vocab:
        st.subheader("📚 Context-Related Vocabulary (Numbered)")
        for i, word in enumerate(st.session_state.vocab, start=1):
            st.write(f"{i}. {word}")

    with col_grammar:
        st.subheader("🔧 Advanced Grammar Structures (Numbered)")
        for i, g in enumerate(st.session_state.grammar, start=1):
            st.write(f"{i}. {g}")

    # Essay below
    st.subheader("📝 Band-9 Sample Essay")
    st.markdown(st.session_state.essay)
