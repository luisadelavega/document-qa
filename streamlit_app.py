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
st.button("➕ Add another url", on_click=add_textbox)

st.write("---")

device_choice = st.selectbox(
    "Choose which version to review:",
    ["Desktop", "Mobile", "Both"],
    index=0
)

# Convert dropdown choice into device_modes list
if device_choice == "Both":
    device_modes = ["desktop", "mobile"]
elif device_choice == "Mobile":
    device_modes = ["mobile"]
else:
    device_modes = ["desktop"]

ALLOWED_DOMAINS = [
    "berevera.com",
    "be-arabelle.com",
    "be-inova.com"
]
# ⭐ Review button is now PRIMARY and gets the green color
# --- REVIEW BUTTON ---
if st.button("Review", type="primary"):
    st.subheader("Review results")

    for idx, text in enumerate(st.session_state.funnel_inputs, start=1):

        st.write(f"### URL {text}")

        # --- Domain validation ---
        if not any(domain in text for domain in ALLOWED_DOMAINS):
            st.error("❌ This domain cannot be reviewed.")
            st.write("---")
            continue

        # --- Run analysis for each selected device type ---
        for device in device_modes:
            with st.spinner(f"Reviewing {device} version... Please wait ⏳"):

                try:
                    full_text = scrape_full_text(text, device=device)
                    analysis = analyze_language_and_errors(full_text)

                    st.success(f"✔ Review complete ({device})")
                    st.write(analysis)

                except Exception as e:
                    st.error(f"❌ Error reviewing {device} version.")
                    st.write(f"Details: `{e}`")

        st.write("---")