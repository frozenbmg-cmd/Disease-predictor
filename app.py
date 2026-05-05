import streamlit as st
import os
from model import train_and_save, load_model
from auth import register, login, save_history, get_history

# ---------- MODEL ----------
if not os.path.exists("model.pkl"):
    train_and_save()

model = load_model()

st.set_page_config(page_title="AI Health Predictor", page_icon="🧠")

# ---------- UI STYLE ----------
st.markdown("""
<style>
body { background-color: #0E1117; }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("🧠 AI Health Predictor")
st.caption("Smart disease prediction using machine learning")

# ---------- SMART NLP ----------
def extract(text):
    text = text.lower()

    symptom_dict = {
        "fever": ["fever", "temperature", "high temp"],
        "cough": ["cough", "cold", "dry cough"],
        "headache": ["headache", "head pain"],
        "fatigue": ["fatigue", "tired", "weak"],
        "body_pain": ["body pain", "body ache"],
        "diarrhea": ["diarrhea", "loose motion"],
        "vomiting": ["vomit", "vomiting"],
        "sore_throat": ["throat", "sore throat"],
        "chills": ["chill", "shiver"],
        "nausea": ["nausea"],
        "runny_nose": ["runny nose", "running nose"],
        "congestion": ["blocked nose", "congestion"],
        "sneezing": ["sneeze", "sneezing"],
        "dizziness": ["dizziness", "light headed"],
        "abdominal_pain": ["stomach", "abdominal", "bloating", "gas"],
        "chest_pain": ["chest pain"],
        "breathlessness": ["breath", "breathing issue"],
        "rash": ["rash"],
        "itching": ["itch", "itching"],
        "weight_loss": ["weight loss"],
        "loss_of_appetite": ["appetite", "not eating"]
    }

    features = []
    for key in symptom_dict:
        found = any(word in text for word in symptom_dict[key])
        features.append(int(found))

    return features

# ---------- AUTH ----------
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.subheader("🔐 Login / Register")

    mode = st.selectbox("Mode", ["Login", "Register"])
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if mode == "Register":
        if st.button("Register"):
            if register(u, p):
                st.success("Registered successfully")
            else:
                st.error("User already exists")

    else:
        if st.button("Login"):
            if login(u, p):
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Invalid login")

# ---------- MAIN ----------
else:
    st.sidebar.title(f"👤 {st.session_state.user}")
    page = st.sidebar.radio("Menu", ["Chat", "History", "About"])

    # ---------- CHAT ----------
    if page == "Chat":
        st.subheader("🩺 Describe your symptoms")

        user_input = st.text_input("Example: fever, headache, body pain")

        if st.button("Predict"):
            f = extract(user_input)

            probs = model.predict_proba([f])[0]
            diseases = model.classes_

            results = list(zip(diseases, probs))
            results.sort(key=lambda x: x[1], reverse=True)

            # Remove healthy if symptoms exist
            if sum(f) >= 2:
                results = [r for r in results if r[0].lower() != "healthy"]

            top3 = results[:3]

            # ---------- RESULT UI ----------
            st.markdown("## 🩺 Prediction Result")

            for i, (d, p) in enumerate(top3):
                color = "#00C853" if i == 0 else "#FFD600" if i == 1 else "#FF5252"

                st.markdown(f"""
                <div style="
                    background: #1e1e2f;
                    padding: 20px;
                    border-radius: 12px;
                    margin-bottom: 10px;
                    box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
                ">
                    <h3 style="color:{color};">{i+1}. {d}</h3>
                    <p style="color:#aaa;">Confidence: {round(p*100,2)}%</p>
                </div>
                """, unsafe_allow_html=True)

            # ---------- DISCLAIMER ----------
            st.info("⚠️ This is not a medical diagnosis. Please consult a doctor.")

            save_history(st.session_state.user, {
                "input": user_input,
                "result": top3[0][0]
            })

    # ---------- HISTORY ----------
    elif page == "History":
        st.subheader("📜 Prediction History")

        history = get_history(st.session_state.user)[::-1]

        for item in history:
            st.markdown(f"""
            <div style="
                background: #1e1e2f;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 10px;
            ">
                <b>🧾 Input:</b> {item['input']}<br>
                <b>🩺 Result:</b> {item['result']}
            </div>
            """, unsafe_allow_html=True)

    # ---------- ABOUT ----------
    else:
        st.subheader("ℹ️ About")
        st.write("AI-based disease prediction system using machine learning and NLP.")
