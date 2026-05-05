import streamlit as st
import os
from model import train_and_save, load_model
from auth import register, login, save_history, get_history

# ---------- MODEL ----------
if not os.path.exists("model.pkl"):
    train_and_save()

model = load_model()

st.set_page_config(page_title="AI Health System")

# ---------- NLP ----------
def extract(text):
    text = text.lower()

    return [
        int("fever" in text),
        int("cough" in text or "cold" in text or "running nose" in text),
        int("headache" in text),
        int("fatigue" in text or "tired" in text),
        int("body pain" in text),
        int("diarrhea" in text),
        int("vomit" in text),
        int("throat" in text),
        int("chill" in text),
        int("nausea" in text),
        int("runny nose" in text),
        int("congestion" in text),
        int("sneeze" in text),
        int("dizziness" in text),
        int("abdominal" in text or "stomach" in text or "bloating" in text),
        int("chest pain" in text),
        int("breath" in text),
        int("rash" in text),
        int("itch" in text),
        int("weight loss" in text),
        int("appetite" in text)
    ]

# ---------- AUTH ----------
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.title("Login / Register")

    mode = st.selectbox("Mode", ["Login","Register"])
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if mode == "Register":
        if st.button("Register"):
            if register(u,p):
                st.success("Registered")
            else:
                st.error("User exists")

    else:
        if st.button("Login"):
            if login(u,p):
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Invalid login")

else:
    st.sidebar.title(st.session_state.user)
    page = st.sidebar.radio("Menu",["Chat","History"])

    if page == "Chat":
        st.title("AI Health Assistant")

        user_input = st.text_input("Enter symptoms")

        if st.button("Predict"):
            f = extract(user_input)

            probs = model.predict_proba([f])[0]
            diseases = model.classes_

            results = list(zip(diseases, probs))
            results.sort(key=lambda x: x[1], reverse=True)

            # remove healthy if symptoms exist
            if sum(f) >= 2:
                results = [r for r in results if r[0].lower() != "healthy"]

            top = results[0][0]

            st.success(f"Predicted: {top}")

            save_history(st.session_state.user, {
                "input": user_input,
                "result": top
            })

    elif page == "History":
        st.title("History")
        for item in get_history(st.session_state.user)[::-1]:
            st.write(f"{item['input']} → {item['result']}")