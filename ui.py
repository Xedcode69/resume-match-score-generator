import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")

URL = f"{base_url}/scan"

st.set_page_config("Resume_scanner")
st.title("Resume Scanner")

with st.form("resume_scanner_form"):
    jd = st.text_area("Enter job description ")
    uploaded_pdf = st.file_uploader("Upload resume PDF", ["pdf"])
    submit = st.form_submit_button("Submit")


if submit:
    if jd and uploaded_pdf:
        st.success("Inputs received. Scanning resume...")
        try:
            with st.spinner("Processing..."):
                response = requests.post(URL, params={"jd": jd, "file": uploaded_pdf})

            if response.status_code == 200:
                data = response.json()
                score = round(data["Matching score"])
                st.progress(score, "Match score: ")
                st.write(f"{score}%")
            else:
                st.error("API error!")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

    else:
        st.error("Input error")
