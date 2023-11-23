import streamlit as st
import mysql.connector
from DocHomeScreen import doc_home_screen
from DocRegister import doc_registration
from DocLogin import doc_login
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

def doctor_functionality():
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

def patient_functionality():
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

def main():
    st.title("Hospital Management System🏥")
    user_type = st.radio("Select user type:", ["Doctor", "Patient"])

    if user_type == "Doctor":
        doctor_functionality()
    elif user_type == "Patient":
        patient_functionality()

if __name__ == "__main__":
    main()
