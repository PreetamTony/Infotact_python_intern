import streamlit as st
import speech_recognition as sr
import pyttsx3
import sqlite3
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import hashlib
import smtplib
from email.mime.text import MIMEText

# Initialize speech and recognition engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Database setup
def init_db():
    """Initialize the SQLite database with users and attendance tables."""
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    # Users table for authentication
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT)''')
    # Attendance table for recording attendance
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  timestamp TEXT,
                  event TEXT)''')
    conn.commit()
    conn.close()

# Hash password for security
def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# Add new user to the database
def add_user(username, password):
    """Add a new user with a hashed password to the database."""
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    try:
        hashed_pw = hash_password(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        st.success(f"User {username} added successfully.")
    except sqlite3.IntegrityError:
        st.error("Username already exists.")
    finally:
        conn.close()

# Authenticate user
def authenticate(username, password):
    """Verify user credentials against the database."""
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result and result[0] == hash_password(password)

# Mark attendance in the database
def mark_attendance(name, event="General"):
    """Record attendance with the given name, event, and timestamp."""
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO attendance (name, timestamp, event) VALUES (?, ?, ?)", (name, timestamp, event))
    conn.commit()
    conn.close()
    return True

# Get attendance data from the database
def get_attendance_data(name=None, event=None):
    """Retrieve attendance data, optionally filtered by name and event."""
    conn = sqlite3.connect('attendance.db')
    query = "SELECT name, timestamp, event FROM attendance"
    params = []
    if name:
        query += " WHERE name=?"
        params.append(name)
    if event:
        query += " WHERE event=?" if not name else " AND event=?"
        params.append(event)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# Voice recognition with language support
def listen(language="en-US"):
    """Capture and recognize voice input with the specified language."""
    with sr.Microphone() as source:
        st.write("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        st.write("Listening...")
        audio = recognizer.listen(source, timeout=5)
        try:
            text = recognizer.recognize_google(audio, language=language)
            st.write(f"Recognized: {text}")
            return text.lower()
        except sr.UnknownValueError:
            st.write("Sorry, I didn't catch that.")
            return None
        except sr.RequestError as e:
            st.write(f"Speech service error: {e}")
            return None

# Text-to-speech feedback
def speak(text):
    """Provide voice feedback using text-to-speech."""
    engine.say(text)
    engine.runAndWait()

# Simulated email notification (placeholder)
def send_notification(to_email, message):
    """Simulate sending an email notification (replace with actual SMTP setup)."""
    st.write(f"Simulated email sent to {to_email}: {message}")

# Main Streamlit UI
def main():
    st.set_page_config(page_title="Enhanced Attendance System", layout="wide")
    st.title("Enhanced Voice Assistant Attendance System")
    init_db()

    # Session state for authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None

    # Authentication: Login or Sign Up
    if not st.session_state.authenticated:
        auth_mode = st.radio("Select Mode", ["Login", "Sign Up"])
        
        if auth_mode == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Logged in successfully!")
                else:
                    st.error("Invalid credentials")
        
        elif auth_mode == "Sign Up":
            st.subheader("Create New Account")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            if st.button("Create Account"):
                if not new_username:
                    st.error("Username cannot be empty.")
                elif not new_password:
                    st.error("Password cannot be empty.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    add_user(new_username, new_password)
        return

    # Tabs for navigation after login
    tab1, tab2, tab3, tab4 = st.tabs(["Attendance", "Reports", "Analytics", "Settings"])

    # Attendance Tab
    with tab1:
        st.header("Mark Attendance")
        event = st.text_input("Event/Class Name (optional)", "General")
        language = st.selectbox("Language", ["en-US", "es-ES", "fr-FR"])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Voice Recognition"):
                name = listen(language)
                if name and mark_attendance(name, event):
                    speak(f"Attendance marked for {name} in {event}.")
                    st.success(f"Attendance marked for {name} in {event}.")
                    send_notification("user@example.com", f"Attendance marked for {name} at {datetime.datetime.now()}")
                else:
                    speak("Error marking attendance.")
                    st.error("Error or unrecognized input.")
        
        with col2:
            manual_name = st.text_input("Manual Entry Name")
            if st.button("Mark Manually"):
                if mark_attendance(manual_name, event):
                    speak(f"Attendance marked for {manual_name} in {event}.")
                    st.success(f"Attendance marked for {manual_name} in {event}.")
                else:
                    st.error("Error marking attendance.")

    # Reports Tab
    with tab2:
        st.header("Attendance Reports")
        report_name = st.text_input("Enter name to filter (leave blank for all):")
        report_event = st.text_input("Enter event to filter (leave blank for all):")
        if st.button("Generate Report"):
            df = get_attendance_data(report_name, report_event)
            st.dataframe(df)
            if not df.empty:
                st.download_button("Download CSV", df.to_csv(index=False), "attendance_report.csv")

    # Analytics Tab
    with tab3:
        st.header("Attendance Analytics")
        df = get_attendance_data()
        if not df.empty:
            fig, ax = plt.subplots()
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.groupby(df['timestamp'].dt.date)['name'].count().plot(kind='bar', ax=ax)
            ax.set_title("Attendance by Date")
            ax.set_xlabel("Date")
            ax.set_ylabel("Count")
            st.pyplot(fig)
        else:
            st.write("No data available for analytics.")

    # Settings Tab
    with tab4:
        st.header("Settings")
        if st.session_state.username == "admin":  # Admin privileges
            st.subheader("Add New User")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            if st.button("Add User"):
                add_user(new_username, new_password)
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.success("Logged out successfully.")

if __name__ == "__main__":
    main()