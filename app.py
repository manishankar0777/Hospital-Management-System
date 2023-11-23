import streamlit as st
# from patient import patient_app
#from doctor import doctor_app

st.title("Hospital Management System")

# Sidebar navigation options
user_type = st.sidebar.radio("Select User Type", ("Patient", "Doctor"))

if user_type == "Patient":
    patient_app()
elif user_type == "Doctor":
    doctor_app()
