import streamlit as st
import mysql.connector
from PatientHomeScreen import patient_home_screen

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

# Function to authenticate a patient
def authenticate_patient(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Define your SQL query to check patient credentials
    query = "SELECT * FROM Patient WHERE email = %s AND password = %s"

    # Execute the query with user-provided username and password
    cursor.execute(query, (username, password))

    # Fetch the result
    result = cursor.fetchone()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return result

def patient_login():

    st.title("Patient Login/Signup⚕️")

    # Create login form (username, password) and authenticate against the database
    login_email = st.text_input("Email")
    login_password = st.text_input("Password", type="password")

    if st.button("Login"):
        patient_data = authenticate_patient(login_email, login_password)
        if patient_data:
            # Authentication successful, retrieve patient's email
            patient_email = patient_data[0]  # Assuming email is the first column in the result

            return patient_email
        else:
            st.error("Authentication failed. Please check your email and password.")

    return None




