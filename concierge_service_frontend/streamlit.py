import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

st.title("Concierge Service")

user_input = st.text_area("Enter your request", "Need a sunset-view table for two tonight; gluten-free menu a must")

if st.button("Submit"):
    if user_input.strip() == "":
        st.warning("Please enter a request before submitting.")
    else:
        url = os.getenv("CONCIERGE_API_URL")
        payload = {"input": user_input}

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                st.success(f"Status: {data.get('status')}")
                st.json(data.get("data"))
                st.info(data.get("message"))
            else:
                st.error(f"API returned status code {response.status_code}")
                st.text(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
