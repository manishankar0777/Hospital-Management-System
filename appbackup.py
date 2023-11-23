import streamlit as st
from PatientApp import patient_app
from DocApp import doc_app
from PatientLogin import patient_login
from DocLogin import doc_login
from PatientRegister import patient_registration
from DocRegister import doc_registration

st.title("Hospital Management System")

# Sidebar navigation options
user_type = st.sidebar.radio("Select User Type", ("Patient", "Doctor"))

if user_type == "Patient":
    option = st.sidebar.selectbox("Choose an option", ["Login", "Register"])
    if option == "Login":
        patient_email = patient_login()
        if patient_email:
            patient_app(patient_email)
    elif option == "Register":
        patient_registration()

elif user_type == "Doctor":
    option = st.sidebar.selectbox("Choose an option", ["Login", "Register"])
    if option == "Login":
        doc_email = doc_login()
        if doc_email:
            doc_app(doc_email)
    elif option == "Register":
        doc_registration()