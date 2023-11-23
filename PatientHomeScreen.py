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

def patient_home_screen(patient_email):
    st.title("Welcome🙏")

    # Display patient's name
    patient_name = get_patient_name(patient_email)
    st.write(f"Hello, {patient_name}!")

    # Provide options for doctors to access different features
    radio_button_keys = ["radio_button_" + str(i) for i in range(4)]

    # Use unique keys for each st.radio widget
    selected_option = st.radio(
        "Select an option:",
        ["View Appointments","View Medical History","Book an Appointment","Update/Cancel Appointment"],
        key=radio_button_keys.pop(0),
    )

    if selected_option == "View Appointments":
         view_patient_appointments(patient_email)
    elif selected_option == "View Medical History":
         view_patient_medicalhistory(patient_email)
    elif selected_option == "Book an Appointment":
         book_appointment(patient_email)
    elif selected_option == "Update/Cancel Appointment":
         update_cancel_appointment()

    # Use unique keys for subsequent st.radio widgets
    # for i in range(3):
    #     st.empty()
    #     st.radio("Placeholder", [], key=radio_button_keys.pop(0))


def get_patient_name(patient_email):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = "SELECT name FROM patient WHERE email = %s"
    cursor.execute(query, (patient_email,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if result:
        return result[0]
    else:
        return "Patient"

# Function to view a patient's appointments
def view_patient_appointments(patient_email):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        query = "SELECT id, date, starttime, endtime, status FROM Appointment WHERE id IN (SELECT appt FROM PatientsAttendAppointments WHERE patient = %s)"
        cursor.execute(query, (patient_email,))
        appointments = cursor.fetchall()

        # Display the appointments if there are any
        if appointments:
            st.subheader("Your Appointments")
            for appointment in appointments:
                st.write(f"Appointment ID: {appointment[0]}")
                st.write(f"Date: {appointment[1]}")
                st.write(f"Time: {appointment[2]} - {appointment[3]}")
                st.write(f"Status: {appointment[4]}")
        else:
            st.write("You have no appointments.")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def view_patient_medicalhistory(patient_email):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        query = "SELECT id, date, conditions, surgeries, medication FROM medicalhistory WHERE id IN (SELECT appt FROM PatientsAttendAppointments WHERE patient = %s);"
        cursor.execute(query, (patient_email,))
        medicalhistory = cursor.fetchone()

        # Display the appointments if there are any
        if medicalhistory:
            st.subheader("Your MedicalHistory")
            st.write(f"Appointment ID: {medicalhistory[0]}")
            st.write(f"Date: {medicalhistory[1]}")
            st.write(f"Conditions: {medicalhistory[2]}")
            st.write(f"Surgeries: {medicalhistory[3]}")
            st.write(f"Medication: {medicalhistory[4]}")
        else:
            st.write("You have no medicalhistory.")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to check for appointment clashes
def check_appointment_clash(selected_date, start_time, end_time):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Check if there are overlapping appointments for the selected date and time
        query = "SELECT id FROM Appointment WHERE date = %s AND ((starttime <= %s AND endtime >= %s) OR (starttime >= %s AND starttime <= %s))"
        cursor.execute(query, (selected_date, start_time, start_time, start_time, end_time))
        conflicting_appointments = cursor.fetchall()

        return len(conflicting_appointments) > 0
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return True
    finally:
        cursor.close()
        conn.close()

# Function to book an appointment
def book_appointment(patient_email):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Create placeholders for selected appointment details
    selected_id = st.number_input("Enter an ID",value=0,step=1)
    # st.write(selected_id)
    selected_date = st.date_input("Select Date")
    # st.write(selected_date)
    start_time = st.time_input("Start Time")
    # st.write(start_time)
    end_time = st.time_input("End Time")
    # st.write(end_time)
    concerns= st.text_input("Concerns")
    symptoms = st.text_input("Symptoms")

    try:
        # Check for appointment clashes before booking
        if check_appointment_clash(selected_date, start_time, end_time):
            st.error("Appointment clash detected. Please choose a different time slot.")
        else:
            # Book the appointment
            insert_query1 = "INSERT INTO Appointment (id, date, starttime, endtime, status) VALUES (%s, %s, %s, %s, 'Done')"
            appointment_data1 = (selected_id, selected_date, start_time, end_time)
            insert_query2 = "INSERT INTO PatientsAttendAppointments (patient, appt,concerns,symptoms) VALUES (%s,%s,%s,%s)"
            appointment_data2 = (patient_email, selected_id,concerns,symptoms)
            cursor.execute(insert_query1, appointment_data1)
            conn.commit()
            cursor.execute(insert_query2, appointment_data2)
            conn.commit()
            st.success("Appointment booked successfully")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to update an appointment
def update_appointment(appointment_id, selected_date, start_time, end_time):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Update the appointment details in the database
        update_query = "UPDATE Appointment SET date = %s, starttime = %s, endtime = %s WHERE id = %s"
        appointment_data = (selected_date, start_time, end_time, appointment_id)

        cursor.execute(update_query, appointment_data)
        conn.commit()

        st.success("Appointment updated successfully")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to cancel an appointment
def cancel_appointment(appointment_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Mark the appointment as canceled in the database
        update_query = "UPDATE Appointment SET status = 'Cancelled' WHERE id = %s"

        cursor.execute(update_query, (appointment_id,))
        conn.commit()

        st.success("Appointment cancelled successfully")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to update or cancel an appointment
def update_cancel_appointment():
    st.subheader("Update or Cancel Appointment")
    appointment_id = st.number_input("Enter the ID of the appointment you want to update or cancel")

    if st.button("Update"):
        
        new_date = st.date_input("Select New Date")
        new_start_time = st.time_input("Select New Start Time")
        new_end_time = st.time_input("Select New End Time")

        # Update the appointment
        update_appointment(appointment_id, new_date, new_start_time, new_end_time)

    if st.button("Cancel"):
        # Cancel the appointment
        cancel_appointment(appointment_id)


