import streamlit as st
import requests

st.title("🎥 AI Movie Matchmaker")

user_id = st.number_input("Enter your User ID", min_value=1, step=1)

if st.button("Get Personalized Recommendations"):
    with st.spinner("Fetching recommendations..."):
        try:
            response = requests.get("http://localhost:5000/recommend", params={"user_id": user_id})
            if response.status_code == 200:
                results = response.json()
                if results:
                    st.subheader("Recommended Movies:")
                    for movie in results:
                        st.markdown(f"🎬 **{movie['title']}** — Similarity Score: {movie['score']}")
                else:
                    st.warning("No recommendations found. Try rating more movies.")
            else:
                st.error("Server error. Make sure the Flask backend is running.")
        except Exception as e:
            st.error(f"Request failed: {e}")
