import streamlit as st
import requests

st.title("Role-Based Chatbot with RAG")

if 'username' not in st.session_state:
    st.session_state['username'] = None
    st.session_state['role'] = None

if not st.session_state['username']:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post("http://localhost:8000/login", json={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state['username'] = username
            st.session_state['role'] = response.json()['role']
            st.success("Logged in successfully!") 
        else:
            st.error("Invalid credentials")
else:
    st.subheader(f"Hello {st.session_state['username']} ({st.session_state['role']})")
    query = st.text_input("Ask your question")

    if st.button("Submit"):
        response = requests.post("http://localhost:8000/query", json={"username": st.session_state['username'], "query": query})
        if response.status_code == 200:
            answer = response.json()['answer']
            sources = response.json()['sources']
            st.write(f"**Answer:** {answer}")
            st.write(f"**Sources:** {', '.join(sources)}")
        elif response.status_code == 401:
            st.warning("Session expired. Please log in again.")
            st.session_state['username'] = None
            st.session_state['role'] = None       
        else:
            st.error("Error processing query")

    if st.button("Logout"):
        st.session_state['username'] = None
        st.session_state['role'] = None
        st.session_state['logged_in'] = False 
        st.rerun()