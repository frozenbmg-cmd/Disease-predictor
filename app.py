import streamlit as st
import os
import numpy as np
from model import train_and_save, load_model
from auth import register, login, save_history, get_history

# ---------- MODEL ----------
if not os.path.exists("model.pkl"):
    train_and_save()

model = load_model()

st.set_page_config(page_title="AI Health Predictor")

# ---------- NLP (STRICT MATCH WITH DATASET) ----------
def extract(text):
    text = text.lower()

    def has(words):
        return int(any(w in text for w in words))

    return [
        has(["fever","temperature"]),
        has(["cough","cold","running nose"]),
        has(["headache"]),
        has(["fatigue","tired","weak"]),
        has(["body pain","body ache"]),
        has(["diarrhea","loose motion"]),
        has(["vomit","vomiting"]),
        has(["throat","sore throat"]),
        has(["chill","shiver"]),
        has(["nausea"]),
        has(["runny nose","running nose"]),
        has(["congestion","blocked nose"]),
        has(["sneeze","sneezing"]),
        has(["dizziness","light headed"]),
        has(["stomach","abdominal","bloating","gas"]),
        has(["chest pain"]),
        has(["breath","breathing issue"]),
        has(["rash"]),
        has(["itch","itching"]),
        has(["weight loss"]),
        has(["appetite","loss of appetite"])
    ]

# ---------- RULE CORRECTION ----------
def apply_rules(results, f):
    diarrhea, vomiting, nausea, abdominal = f[5], f[6], f[9], f[14]

    # If stomach symptoms → prioritize correct diseases
    if abdominal and (vomiting or nausea or diarrhea):
        priority = {"Food Poisoning", "Stomach Infection"}
        results = sorted(results, key=lambda x: (x[0] not in priority, -x[1]))

    return results

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

# ---------- MAIN ----------
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

            # smooth probabilities
            probs = np.round(probs, 4)

            results = list(zip(diseases, probs))
            results.sort(key=lambda x: x[1], reverse=True)

            # remove healthy if real symptoms present
            if sum(f) >= 2:
                results = [r for r in results if r[0].lower() != "healthy"]

            # apply correction rules
            results = apply_rules(results, f)

            top3 = results[:3]

            st.subheader("Prediction Result")

            for i, (d, p) in enumerate(top3):
                st.write(f"{i+1}. {d} ({round(p*100,2)}%)")

            st.info("This is not a medical diagnosis. Consult a doctor.")

            save_history(st.session_state.user, {
                "input": user_input,
                "result": top3[0][0]
            })

    elif page == "History":
        st.title("History")
        for item in get_history(st.session_state.user)[::-1]:
            st.write(f"{item['input']} → {item['result']}")
