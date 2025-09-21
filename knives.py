import streamlit as st
import hashlib
# streamlit run C:\Users\shayn\Python\Knives2\knives.py

# Initialize Username Variable
st.session_state.username = ""

# Hash Password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Does User Name Exist?
def check_username(username, filename='users.txt'):
    try:
        with open(filename, 'r') as file:
            for line in file:
                stored_username = line.strip().split(',')[0]
                if stored_username.lower() == username.lower():
                    return True  # username already exists
        return False  # username available
    except FileNotFoundError:
        print("    File not found.")

# Create Account
def create_account(username, password, filename='users.txt'):
    if not check_username(username, filename):
        hashed_password = hash_password(password)
        with open(filename, 'a') as file:
            file.write(f'{username},{hashed_password}\n')
        return True  # account created successfully
    else:
        return False  # username already exists

# Log In
def login(username, password, filename='users.txt'):
    try:
        with open(filename, 'r') as file:
            for line in file:
                stored_username, stored_hashed_password = line.strip().split(',')
                if stored_username == username:
                    hashed_password = hash_password(password)
                    if hashed_password == stored_hashed_password:
                        return True  # login successful
                    else:
                        return False  # incorrect password
        return False  # username does not exist
    except FileNotFoundError:
        return False  # file does not exist

# Set page config to scale to screen size
st.set_page_config(layout="wide")

# Home page
def home_page():
    st.title("Home")
    with st.form("sign_in_form"):
        username = st.text_input("User Name")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In")
        if submitted:
            if check_username(username):
                if login(username, password):
                    st.session_state.page = "logged_in"
                else:
                    st.error("Incorrect password")
            else:
                st.error("Username not found")
    if st.button("Sign Up"):
         st.session_state.page = "sign_up"

# Sign up page
def signup_page():
    st.title("Sign Up")
    with st.form("signup_form"):
        username = st.text_input("User Name")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Re-Enter Password", type="password")
        if st.button("Submit"):
            if check_username(username):
                st.error("Username already exists")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                create_account(username, password)
                st.session_state.page = "home"
                st.session_state.logged_in = True
                st.session_state.username = username

# Main page
def main_page():
    st.title("Welcome " + st.session_state.username)

# Initialize page state
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Render pages
if st.session_state.page == "home":
    if st.session_state.logged_in:
        main_page()
    else:
        home_page()
elif st.session_state.page == "signup":
    signup_page()
else:
    main_page()
