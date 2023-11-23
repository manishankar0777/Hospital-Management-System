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

def doc_registration():
    st.title("Doctor Registration")
    
    doc_email=st.text_input("Email ID",key="c")
    doc_gender=st.radio("Gender",('Male','Female','Other'))
    doc_password=st.text_input("Create a Password",type='password',key='password')
    doc_name=st.text_input("Enter Name",key="a")


    if st.button("Register"):
        conn=connect_to_database()
        cursor=conn.cursor()

        try:
            # Create a new patient record in the database
            insert_query = "INSERT INTO Doctor (email,gender,password,name) VALUES (%s, %s, %s, %s)"
            doc_data = (doc_email,doc_gender,doc_password,doc_name)
            
            cursor.execute(insert_query, doc_data)
            conn.commit()
            
            st.success("Doctor registered successfully")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()


doc_registration()
