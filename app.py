
import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="Vedic Astro Dashboard", layout="centered")
st.title("🪐 Vedic Astro-Tech Forecast Dashboard")

# --- Weekly Forecast Section ---
st.header("🗓️ Weekly Forecast")
today = datetime.date.today()
start_of_week = today - datetime.timedelta(days=today.weekday())
end_of_week = start_of_week + datetime.timedelta(days=6)

weekly_text = f'''
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
st.markdown(weekly_text)

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

# --- Email Notification Placeholder ---
st.header("📧 Weekly Email Forecast")
email = st.text_input("Enter your email to receive weekly forecasts:")
password = st.text_input("Email App Password (not stored)", type="password")
send_now = st.button("Send Test Email")

if send_now and email and password:
    try:
        msg = MIMEText(weekly_text)
        msg['Subject'] = "Your Weekly Vedic Forecast"
        msg['From'] = email
        msg['To'] = email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
        server.sendmail(email, [email], msg.as_string())
        server.quit()

        st.success("Forecast sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")
