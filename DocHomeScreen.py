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

def doc_home_screen(doc_email):
    st.title("Welcome, Doctor 🙏")

    # Display doctor's name
    doc_name = get_doctor_name(doc_email)
    st.write(f"Hello, {doc_name}!")

    # Provide options for doctors to access different features
    radio_button_keys = ["radio_button_" + str(i) for i in range(3)]

    # In doc_home_screen or related functions
    selected_option = st.radio(
    "Select an option:",
    ["View Appointments", "View Patient Profiles", "Diagnose and Prescribe"],
    key=radio_button_keys.pop(0),
    )

    if selected_option == "View Appointments":
        view_appointments(doc_email)
    elif selected_option == "View Patient Profiles":
        view_patient_profiles()
    elif selected_option == "Diagnose and Prescribe":
        diagnose_and_prescribe(doc_email)

def get_doctor_name(doc_email):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = "SELECT name FROM Doctor WHERE email = %s"
    cursor.execute(query, (doc_email,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if result:
        return result[0]
    else:
        return "Doctor"

def view_appointments(doc_email):
    st.subheader("Appointments")

    conn = connect_to_database()
    cursor = conn.cursor()

    query = "SELECT A.id, A.date, A.starttime, A.endtime, P.name " \
            "FROM Appointment A " \
            "JOIN PatientsAttendAppointments PAA ON A.id = PAA.appt " \
            "JOIN Patient P ON PAA.patient = P.email " \
            "WHERE A.status = 'Done' AND A.id IN " \
            "(SELECT appt FROM Diagnose WHERE doctor = %s)"
    
    cursor.execute(query, (doc_email,))
    appointments = cursor.fetchall()

    if appointments:
        for appointment in appointments:
            st.write(f"Appointment ID: {appointment[0]}")
            st.write(f"Date: {appointment[1]}")
            st.write(f"Time: {appointment[2]} - {appointment[3]}")
            st.write(f"Patient: {appointment[4]}")
            st.write("--------------")
    else:
        st.write("No appointments available.")

    cursor.close()
    conn.close()


def view_patient_profiles():
    st.subheader("View Patient Profiles")
    
    # Get a list of all patients
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT email, name FROM Patient")
    patients = cursor.fetchall()
    
    # Create a select box for the doctor to choose a patient
    selected_patient = st.selectbox("Select a patient:", [f"{patient[1]} ({patient[0]})" for patient in patients])
    
    # Extract the email from the selected option
    selected_patient_email = selected_patient.split(" ")[-1][1:-1]
    
    # Query and display the selected patient's profile
    cursor.execute("SELECT * FROM Patient WHERE email = %s", (selected_patient_email,))
    patient_data = cursor.fetchone()
    
    if patient_data:
        st.write(f"Patient Name: {patient_data[2]}")
        st.write(f"Email: {patient_data[0]}")
        st.write(f"Address: {patient_data[3]}")
        st.write(f"Gender: {patient_data[4]}")
    else:
        st.write("Patient not found.")

    cursor.close()
    conn.close()

def diagnose_and_prescribe(doc_email):
    st.subheader("Diagnose and Prescribe")
    
    # Get a list of patients with appointments for the doctor
    conn = connect_to_database()
    cursor = conn.cursor()
    
    # Query the appointments for the doctor
    cursor.execute("SELECT A.id, P.name FROM Appointment A " 
                   "JOIN PatientsAttendAppointments PAA ON A.id = PAA.appt "
                   "JOIN Patient P ON PAA.patient = P.email " 
                   "WHERE A.status = 'Done' AND A.id IN "
                   "(SELECT appt FROM Diagnose WHERE doctor = %s)", (doc_email,))
    appointments = cursor.fetchall()
    
    if appointments:
        selected_appointment = st.selectbox("Select an appointment to diagnose and prescribe:", 
                                             [f"Appointment ID: {appointment[0]}, Patient: {appointment[1]}" for appointment in appointments])
        
        # Extract the appointment ID from the selected option
        selected_appointment_id = int(selected_appointment.split(":")[1].split(",")[0])
        
        # Create text input fields for diagnosis and prescription
        diagnosis = st.text_input("Diagnosis:")
        prescription = st.text_input("Prescription:")
        
        if st.button("Submit Diagnosis and Prescription"):
            try:
                # Insert diagnosis and prescription into the Diagnose table
                cursor.execute("INSERT INTO Diagnose (appt, doctor, diagnosis, prescription) "
                               "VALUES (%s, %s, %s, %s)",
                               (selected_appointment_id, doc_email, diagnosis, prescription))
                conn.commit()
                st.success("Diagnosis and prescription added successfully.")
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
    else:
        st.write("No appointments available for diagnosis and prescription.")

    cursor.close()
    conn.close()



