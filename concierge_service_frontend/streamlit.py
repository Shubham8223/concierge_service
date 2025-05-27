import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

st.title("Concierge Service")

user_input = st.text_area("Enter your request", "")
is_input_valid = user_input.strip() != ""

if st.button("Submit", disabled=not is_input_valid):
    if user_input.strip() == "":
        st.warning("Please enter a request before submitting.")
    else:
        url = os.getenv("CONCIERGE_API_URL")
        payload = {"input": user_input}

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                data = result.get("data", {})

                st.success(f"Status: {result.get('status')}")
                st.info(result.get("message"))
     
                if data.get('intent_category', 'N/A')=="N/A":
                    st.subheader("Web Search Results")
                    web_search_results = data.get("web_search_results", [])
                    if web_search_results:
                        for item in web_search_results:
                            title = item.get("title", "No title")
                            snippet = item.get("snippet", "No snippet available")
                            url = item.get("url", "No URL available")
                            st.markdown(f"### {title}")
                            st.write(snippet)
                            st.write(f"[Read more]({url})")
                    else:
                        st.write("No web search results found.")
                    
                else: 
                    
                    # Intent Info
                    st.subheader("Intent Information")
                    st.write(f"**Intent Category:** {data.get('intent_category', 'N/A')}")
                    st.write(f"**Confidence Score:** {data.get('confidence_score', 'N/A')}")

                    # Entities
                    st.subheader("Entities Extracted")
                    entities = data.get("entities", {})
                    if entities:
                        for key, value in entities.items():
                            st.write(f"**{key.replace('_', ' ').title()}**: {value}")
                    else:
                        st.write("No entities found.")

                    # Follow-Up Questions
                    follow_ups = data.get("follow_up_questions", [])
                    if follow_ups:
                        st.subheader("Follow-Up Questions")
                        with st.form("follow_up_form"):
                            responses = {}
                            for question in follow_ups:
                                field = question.get("field", "")
                                label = f"{question.get('question', '')} {'*' if question.get('required') else ''}"
                                options = question.get("options", [])

                                if options:
                                    response = st.selectbox(label, options, key=field)
                                else:
                                    response = st.text_input(label, key=field)

                                responses[field] = response

                            submitted = st.form_submit_button("Submit Follow-Up Answers")
                            if submitted:
                                st.success("Follow-up responses submitted:")
                                st.json(responses)
                    else:
                        st.write("No follow-up questions.")
            else:
                st.error(f"API returned status code {response.status_code}")
                st.text(response.json()["error"])
        except Exception as e:
            st.error(f"An error occurred: {e}")
