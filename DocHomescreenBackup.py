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

def authenticate_doctor(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    # Define your SQL query to check patient credentials
    query = "SELECT * FROM Doctor WHERE email = %s AND password = %s"
    
    # Execute the query with user-provided username and password
    cursor.execute(query, (username, password))
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Close cursor and connection
    cursor.close()
    conn.close()
    
    return result

def doc_login():
    st.title("Doctor Login")

    # Create login form (username, password) and authenticate against the database
    login_email = st.text_input("Email")
    login_password = st.text_input("Password", type="password")

    if st.button("Login"):
        doc_data = authenticate_doctor(login_email, login_password)
        if doc_data:
            # Authentication successful, retrieve patient's email
            doc_email = doc_data[0]  # Assuming email is the first column in the result

            # Display the patient's appointments based on their email
            doc_home_screen()
        else:
            st.error("Authentication failed. Please check your email and password.")



