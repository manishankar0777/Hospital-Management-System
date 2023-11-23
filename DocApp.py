import streamlit as st
import mysql.connector
from DocHomeScreen import doc_home_screen
from DocRegister import doc_registration
from DocLogin import doc_login

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


# Function to connect to the database
def connect_to_database():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "dynamo@17",
        "database": "hms",
    }
    conn = mysql.connector.connect(**db_config)
    return conn

def main():
    st.title("Doctor Management System")

    menu = st.radio("Select an option:", ["Login", "Register"])

    if menu == "Login":
        doc_email = doc_login()
        if doc_email:
            st.session_state.logged_in = doc_email
            doc_home_screen(doc_email)
    elif menu == "Register":
        doc_registration()

    if st.session_state.logged_in:
        doc_home_screen(st.session_state.logged_in)

if __name__ == "__main__":
    main()