import streamlit as st
import mysql.connector

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

# Patient registration section
def patient_registration():
    st.subheader("Patient Registration")
    new_patient_email = st.text_input("Email", key="email_input")
    new_patient_password = st.text_input("Password", type="password", key="password_input")
    new_patient_name = st.text_input("Name", key="name_input")
    new_patient_address = st.text_input("Address", key="address_input")
    new_patient_gender = st.radio("Gender", ('Male', 'Female', 'Other'), key="gender_input")

    if st.button("Register",key="register_button"):
        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            # Create a new patient record in the database
            insert_query = "INSERT INTO Patient (email, password, name, address, gender) VALUES (%s, %s, %s, %s, %s)"
            patient_data = (new_patient_email, new_patient_password, new_patient_name, new_patient_address, new_patient_gender)

            cursor.execute(insert_query, patient_data)
            conn.commit()

            st.success("Patient registered successfully")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

patient_registration()