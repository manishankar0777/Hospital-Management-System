import streamlit as st
import mysql.connector
from PatientHomeScreen import patient_home_screen
from PatientRegister import patient_registration
from PatientLogin import patient_login

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
    st.title("Patient Management System")

    menu = st.radio("Select an option:", ["Login","Register"])

    if menu == "Login":
        patient_email = patient_login()
        if patient_email:
            st.session_state.logged_in = patient_email
            patient_home_screen(patient_email)
    elif menu == "Register":
        patient_registration()

    if st.session_state.logged_in:
        patient_home_screen(st.session_state.logged_in)

if __name__ == "__main__":
    main()