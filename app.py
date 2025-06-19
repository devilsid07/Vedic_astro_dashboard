
import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText
from fpdf import FPDF

# UI setup
st.set_page_config(page_title="Vedic Astro Dashboard", layout="centered")
st.title("🪐 Vedic Astro-Tech Forecast Dashboard")

# --- Weekly Forecast Section ---
st.header("🗓️ Weekly Forecast")
today = datetime.date.today()
start_of_week = today - datetime.timedelta(days=today.weekday())
end_of_week = start_of_week + datetime.timedelta(days=6)
weekly_forecast = f'''
**Weekly Forecast ({start_of_week.strftime('%d %B')} – {end_of_week.strftime('%d %B %Y')})**

This week brings a mix of reflection, creativity, and public visibility.

- ✅ **Best Days**:
    - **Wednesday & Thursday**: Great for quiet focus, spiritual work, or soft planning.
    - **Sunday**: Creative expression, design, learning.

- ⚠️ **Be Cautious**:
    - **Friday**: Tense day for finances or sharp words.
    - **Saturday**: Avoid rushing or making big decisions.

- 🌕 **Weekly Themes**:
    - Inner alignment
    - Career or public actions midweek
    - Strategic silence or research

Tip: Journal, plan, and act gently. This is a week to plant seeds, not rush outcomes.
'''
st.markdown(weekly_forecast)

# --- Compatibility Matching Section ---
st.header("💑 Compatibility Matching")
with st.form("compat_form"):
    st.subheader("Person 1")
    dob1 = st.date_input("Date of Birth 1", datetime.date(1990, 1, 1))
    tob1 = st.time_input("Time of Birth 1", datetime.time(10, 0))
    lat1 = st.number_input("Latitude 1", value=25.45, key='lat1')
    lon1 = st.number_input("Longitude 1", value=81.84, key='lon1')
    tz1 = st.number_input("Timezone 1", value=5.5, key='tz1')

    st.subheader("Person 2")
    dob2 = st.date_input("Date of Birth 2", datetime.date(1992, 2, 2))
    tob2 = st.time_input("Time of Birth 2", datetime.time(12, 0))
    lat2 = st.number_input("Latitude 2", value=25.45, key='lat2')
    lon2 = st.number_input("Longitude 2", value=81.84, key='lon2')
    tz2 = st.number_input("Timezone 2", value=5.5, key='tz2')

    submitted = st.form_submit_button("Compare")
    if submitted:
        st.write("🌓 Moon Sign & Nakshatra matching coming soon...")
        st.success("Basic data captured. Compatibility logic under construction.")

# --- Muhurta Suggestion ---
st.header("📅 Muhurta Finder")
event_type = st.selectbox("Choose Event Type", ["business", "travel"])
event_muhurta_rules = {
    "business": ["Wednesday", "Thursday", "Friday"],
    "travel": ["Monday", "Thursday"]
}
muhurta_list = []
for i in range(14):
    d = today + datetime.timedelta(days=i)
    if d.strftime("%A") in event_muhurta_rules[event_type]:
        muhurta_list.append(d.strftime("%A, %d %B %Y"))
st.write("**Suggested Dates:**")
for date in muhurta_list[:5]:
    st.write("✅", date)

# --- Hora Timing (Sunrise-based placeholder) ---
st.subheader("🕐 Hora Timings for Today")
hora_planets = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
hora_blocks = []
base = datetime.datetime.combine(today, datetime.time(6, 0))
weekday_index = today.weekday()
first_lord = hora_planets[weekday_index % 7]
sequence = hora_planets[hora_planets.index(first_lord):] + hora_planets[:hora_planets.index(first_lord)]
for i in range(24):
    start_time = (base + datetime.timedelta(hours=i)).time().strftime('%H:%M')
    end_time = (base + datetime.timedelta(hours=i+1)).time().strftime('%H:%M')
    planet = sequence[i % 7]
    st.write(f"{start_time} - {end_time} → {planet} Hora")

# --- PDF Export ---
st.header("📄 Export Forecast as PDF")
if st.button("Generate PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Vedic Astro Report", ln=True, align='C')
    pdf.ln(10)
    for line in weekly_forecast.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf_path = "/mnt/data/vedic_forecast_export.pdf"
    pdf.output(pdf_path)
    st.success("PDF created!")
    st.download_button("Download PDF", data=open(pdf_path, "rb"), file_name="vedic_forecast.pdf")

# --- Email Notification ---
st.header("📧 Email This Forecast")
email = st.text_input("Enter your Gmail address:")
password = st.text_input("Gmail App Password", type="password")
if st.button("Send Email"):
    try:
        msg = MIMEText(weekly_forecast)
        msg['Subject'] = "Your Weekly Vedic Forecast"
        msg['From'] = email
        msg['To'] = email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
        server.sendmail(email, [email], msg.as_string())
        server.quit()
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Email failed: {e}")
