import streamlit as st
import requests

# API base URL
BASE_URL = "http://127.0.0.1:8000"

# Streamlit UI
st.title("Gamified Chat Application")

# Session state to hold authentication token and user info
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None

# Helper function for API requests
def api_request(endpoint, method="GET", data=None, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    if method == "GET":
        return requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    elif method == "POST":
        return requests.post(f"{BASE_URL}{endpoint}", json=data, headers=headers)
    else:
        return None

# Authentication Section
st.sidebar.header("Authentication")
auth_option = st.sidebar.radio("Choose Action", ["Login", "Register"])

if auth_option == "Register":
    st.sidebar.subheader("Register")
    reg_username = st.sidebar.text_input("Username", key="reg_username")
    reg_password = st.sidebar.text_input("Password", type="password", key="reg_password")
    if st.sidebar.button("Register"):
        response = api_request("/users/register", method="POST", data={"username": reg_username, "password": reg_password})
        if response.status_code == 200:
            st.sidebar.success("Registered successfully! Please log in.")
        else:
            st.sidebar.error(response.json().get("detail", "Error during registration."))

if auth_option == "Login":
    st.sidebar.subheader("Login")
    login_username = st.sidebar.text_input("Username", key="login_username")
    login_password = st.sidebar.text_input("Password", type="password", key="login_password")
    if st.sidebar.button("Login"):
        response = api_request("/users/login", method="POST", data={"username": login_username, "password": login_password})
        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            st.session_state.username = login_username
            st.sidebar.success(f"Welcome, {login_username}!")
        else:
            st.sidebar.error(response.json().get("detail", "Login failed."))

# Main Application
if st.session_state.token:
    st.subheader(f"Welcome, {st.session_state.username}!")

    # Display Balance
    st.write("### User Balance")
    balance_response = api_request("/currency/balance", token=st.session_state.token)
    if balance_response.status_code == 200:
        st.write(f"Balance: {balance_response.json()['balance']} units")
    else:
        st.error("Unable to fetch balance.")

    # Display Pot
    st.write("### Pot Information")
    pot_response = api_request("/pot/", token=st.session_state.token)
    if pot_response.status_code == 200:
        st.write(f"Pot Amount: {pot_response.json()['pot_amount']} units")
    else:
        st.error("Unable to fetch pot amount.")

    # Send Message
    st.write("### Send Message")
    if st.button("Send Message"):
        message_response = api_request("/messages/send", method="POST", token=st.session_state.token)
        if message_response.status_code == 200:
            result = message_response.json()
            st.write(f"Message: {result['message']}")
            st.write(f"Updated Pot: {result['pot_amount']} units")
        elif message_response.status_code == 400:
            st.error(message_response.json().get("detail", "Error while sending message."))
        else:
            st.error("Unable to send message.")

    # Logout
    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.username = None
        st.experimental_rerun()
