# Infotact_Python_Internship
# Enhanced Attendance System & Currency Converter

## Project 1: Enhanced Voice Assistant Attendance System

### Description
This project is a **voice-powered attendance system** built with **Streamlit**, allowing users to mark attendance using speech recognition. It includes authentication, analytics, and reporting functionalities.

### Features
- **User Authentication**: Secure login and sign-up with password hashing.
- **Voice Recognition**: Uses `speech_recognition` to capture names.
- **Text-to-Speech Feedback**: Confirms attendance using `pyttsx3`.
- **Attendance Recording**: Stores data in an SQLite database.
- **Reports & Analytics**: Generates CSV reports and visualizes attendance trends.
- **Email Notifications**: Simulates sending attendance alerts via email.

### Tech Stack
- **Python**
- **Streamlit** (for UI)
- **SpeechRecognition & pyttsx3** (for voice processing)
- **SQLite3** (for database management)
- **Matplotlib & Pandas** (for analytics)
- **smtplib** (for email notifications)

### Installation & Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Run the application:
   ```sh
   streamlit run smart_attendance.py
   ```

---

## Project 2: Enhanced Currency Converter

### Description
A **GUI-based currency converter** that fetches real-time exchange rates and provides historical trends.

### Features
- **Real-Time Exchange Rates**: Fetches live rates from an API.
- **Historical Trends**: Displays conversion trends using Matplotlib.
- **User-Friendly UI**: Built with Tkinter.
- **Multi-Currency Support**: Convert between various international currencies.

### Tech Stack
- **Python**
- **Tkinter** (for GUI)
- **Requests** (for API calls)
- **Matplotlib** (for plotting trends)
- **JSON** (for data management)

### Installation & Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
   
2. Run the application:
   ```sh
   python currency_converter.py
   ```

---

## Contribution
Feel free to contribute by forking the repository, making changes, and submitting a pull request.

## License
This project is licensed under the MIT License.

