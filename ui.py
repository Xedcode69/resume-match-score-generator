import streamlit as st
import os
import requests

URL = "http://127.0.0.1:8000/scan"

st.set_page_config("Resume_scanner")
st.title("Resume Scanner")

with st.form("resume_scanner_form"):
    jd = st.text_area("Enter job description ")
    uploaded_pdf = st.file_uploader("Upload resume PDF", ["pdf"])
    submit = st.form_submit_button("Submit")


if submit:
    if jd and uploaded_pdf:
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        filepath = os.path.join("uploads", uploaded_pdf.name)

        with open(filepath, "wb") as file:
            file.write(uploaded_pdf.getbuffer())

        st.success("File uploaded successfully")

        try:
            with st.spinner("Processing..."):
                response = requests.get(
                    URL, params={"jd": jd, "name": uploaded_pdf.name}
                )

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
