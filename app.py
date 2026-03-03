import streamlit as st
import requests

API_URL = "https://shl-api-720651928669.us-central1.run.app/recommend"

st.title("SHL Assessment Recommendation Engine")

query = st.text_area("Enter Job Description or Query")

if st.button("Get Recommendations"):

    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Fetching recommendations..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"query": query},
                    timeout=60
                )

                if response.status_code == 200:
                    results = response.json().get("recommended_assessments", [])

                    if results:
                        for i, item in enumerate(results, 1):
                            st.subheader(f"{i}. {item['name']}")
                            st.write(item["description"])
                            st.write(f"Duration: {item['duration']} minutes")
                            st.markdown(f"[Open Assessment]({item['url']})")
                            st.divider()
                    else:
                        st.info("No recommendations found.")

                else:
                    st.error(f"API Error: {response.status_code}")

            except Exception as e:
                st.error(str(e))
