# streamlit_app.py

import streamlit as st
import requests

# 1) Must be the very first Streamlit call
st.set_page_config(page_title="Kannada Tutor", page_icon="📚", layout="wide")

st.title("🌟 Kannada Tutor")

# Sidebar: select backend and mode
API_BASE = st.sidebar.text_input(
    "API Base URL",
    value="http://localhost:8000",
    help="Your FastAPI backend URL"
)
mode = st.sidebar.radio("Mode", ["Learn", "Flashcards", "Quiz"])

# ——— Learn Mode ———
if mode == "Learn":
    st.header("📚 Learn Mode")
    theme = st.text_input("Lesson theme (Kannada or English)", "fruits")
    count = st.slider("Number of sentences", 1, 10, 5)

    if st.button("Generate Lesson"):
        try:
            resp = requests.get(f"{API_BASE}/lesson/", params={"theme": theme, "count": count})
            resp.raise_for_status()
            lessons = resp.json()

            if not lessons:
                st.warning("No lessons returned.")
            else:
                for i, item in enumerate(lessons, start=1):
                    st.markdown(f"**{i}. Kannada:** {item.get('kannada', '—')}")
                    st.markdown(f"> Transliteration: {item.get('transliteration', '—')}")
                    st.markdown(f"> English: {item.get('english', '—')}")

        except Exception as e:
            st.error(f"Lesson error: {e}")

# ——— Flashcards Mode ———
elif mode == "Flashcards":
    st.header("🃏 Flashcards Mode")
    words_input = st.text_input("Enter words (comma-separated Kannada)", "ಮನೆ, ಪುಸ್ತಕ")
    style = st.selectbox("Illustration style", ["cartoon", "watercolor", "sketch"])

    if st.button("Generate Flashcards"):
        words = [w.strip() for w in words_input.split(",") if w.strip()]
        if not words:
            st.warning("Please enter at least one word.")
        else:
            try:
                resp = requests.post(f"{API_BASE}/flashcards/", json={"words": words, "style": style})
                resp.raise_for_status()
                cards = resp.json()

                cols = st.columns(min(len(words), 5))
                for idx, w in enumerate(words):
                    with cols[idx % len(cols)]:
                        data = cards.get(w, {})
                        if data.get("image_url"):
                            st.image(data["image_url"], caption=w, use_column_width=True)
                        else:
                            st.error(data.get("error", "No image returned"))
            except Exception as e:
                st.error(f"Flashcards error: {e}")

# ——— Quiz Mode ———
else:
    st.header("❓ Quiz Mode")
    topic = st.text_input("Enter a topic for your quiz", "vehicles")

    if st.button("Generate Quiz"):
        try:
            resp = requests.post(f"{API_BASE}/quiz/", json={"question": topic})
            resp.raise_for_status()
            data = resp.json()

            if "error" in data:
                st.error(data["error"])
            elif "quiz" not in data:
                st.error("Received unexpected format from the server.")
            else:
                st.subheader(f"📝 Quiz on “{topic}”")
                for idx, q in enumerate(data["quiz"], start=1):
                    st.markdown(f"**Q{idx}: {q['question']}**")
                    # Show choices
                    for letter, choice in q["choices"].items():
                        st.markdown(f"- **{letter}.** {choice}")
                    # Show correct answer
                    correct = q["correct"]
                    ans_text = q["choices"].get(correct, "")
                    st.markdown(f"✅ **Answer: {correct}. {ans_text}**")
                    st.markdown("---")
        except Exception as e:
            st.error(f"Quiz error: {e}")
