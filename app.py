import streamlit as st
from dotenv import load_dotenv
from groq_client import groq_generate
import requests
import os

load_dotenv()
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

st.set_page_config(
    page_title="IELTS Writing Task Generator (Band 9)",
    page_icon="✍️",
    layout="wide"
)

st.title("IELTS Writing Task Generator")
st.caption("Generate context-based vocabulary, grammar structures, and an essay.")


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
    You are an experienced IELTS examiner.

Write a Band-9 IELTS Writing Task 2 essay on the following topic with these rules:

1. Exactly 4 paragraphs: Introduction, Body Paragraph 1, Body Paragraph 2, Conclusion.  
2. Strict word count: **no fewer than 270 words and no more than 300 words**. You **must count words carefully**.  
3. Formal academic tone, precise vocabulary, and varied sentence structures.  
4. Use advanced grammar suitable for Band 8–9 candidates.  
5. Present coherent, logically developed arguments with **specific examples**.  
6. Use strong topic sentences, cohesive devices, and clear progression of ideas.  
7. Avoid contractions and informal language.  
8. At the **end of the essay**, write: “Word count: XXX” with the exact number of words and make it bold.


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

topic = st.text_area(
    "Enter IELTS Writing Task Topic",
    placeholder="Some people believe that technology has made our lives more complicated. Discuss both views and give your opinion.",
    height=120
)

col_main, col_search = st.columns([3, 1])
with col_search:
    search_word = st.text_input("🔍 Search Word")
    if st.button("Search Meaning"):
        if search_word.strip():
            st.session_state.meaning = get_word_meaning(search_word.strip())

if st.session_state.meaning:
    st.info(f"**{search_word.strip()}**: {st.session_state.meaning}")

with col_main:
    generate = st.button("🎯 Generate Content", type="primary")

if generate:
    if not topic.strip():
        st.error("Please enter an IELTS writing task topic.")
    else:
        with st.spinner("Generating IELTS content..."):
            raw = generate_ielts_content(topic)

        st.session_state.vocab = clean_list(raw["vocabulary"])
        st.session_state.grammar = clean_list(raw["grammar"])
        st.session_state.essay = raw["essay"]
        st.session_state.generated = True
        st.success("✅ Content Generated")

if st.session_state.generated:
    col_vocab, col_grammar = st.columns(2)

    with col_vocab:
        st.subheader("📚 Context-Related Vocabulary")
        for i, word in enumerate(st.session_state.vocab, start=1):
            st.write(f"{i}. {word}")

    with col_grammar:
        st.subheader("🔧 Advanced Grammar Structures")
        for i, g in enumerate(st.session_state.grammar, start=1):
            st.write(f"{i}. {g}")

    st.subheader("📝 Sample Essay")
    st.markdown(st.session_state.essay)

# Developed by Sushil Sharma Subedi
st.caption("Developed by Sushil Sharma Subedi")