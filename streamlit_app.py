import streamlit as st
from openai import OpenAI
from functions_reviewer import *

st.set_page_config(page_title="Funnel Reviewer")


# --- CSS: style ONLY primary buttons (Review) ---
st.markdown("""
<style>
/* Streamlit primary button */
button[data-testid="baseButton-primary"] {
    background-color: #4CAF50 !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 0.6rem 1.4rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
}

button[data-testid="baseButton-primary"]:hover {
    background-color: #45a049 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Title and Description ---
st.title("Funnel Reviewer")
st.write("Automatically review all your funnel steps in one go. Just paste your URLs below!")

# --- Session state for text boxes ---
if "funnel_inputs" not in st.session_state:
    st.session_state.funnel_inputs = [""]


def add_textbox():
    st.session_state.funnel_inputs.append("")


# --- Render input boxes ---
for i in range(len(st.session_state.funnel_inputs)):
    st.session_state.funnel_inputs[i] = st.text_input(
        f"Funnel URL {i+1}",
        value=st.session_state.funnel_inputs[i],
        key=f"text_input_{i}",
        placeholder="https://example.com"
    )

# This stays black (default)
st.button("➕ Add another", on_click=add_textbox)

st.write("---")

ALLOWED_DOMAINS = [
    "berevera.com",
    "be-arabelle.com",
    "be-inova.com"
]
# ⭐ Review button is now PRIMARY and gets the green color
if st.button("Review", type="primary"):
    st.subheader("Review results")

    for idx, text in enumerate(st.session_state.funnel_inputs, start=1):

        st.write(f"### URL {text}")

        # --- 1️⃣ Check domain validity ---
        if not any(domain in text for domain in ALLOWED_DOMAINS):
            st.error("❌ This domain cannot be reviewed.")
            st.write("---")
            continue

        # --- 2️⃣ Valid domain → show loading animation ---
        with st.spinner("Reviewing this URL... Please wait ⏳"):

            try:
                full_text = scrape_full_text(text)
                analysis = analyze_language_and_errors(full_text)

                st.success("✔ Review complete!")
                st.write(analysis)

            except Exception as e:
                st.error("❌ Error reviewing this URL.")
                st.write(f"Details: `{e}`")

        st.write("---")