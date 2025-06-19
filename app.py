import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText
from fpdf import FPDF

# UI setup
st.set_page_config(page_title="Vedic Astro Dashboard", layout="centered")
st.title("🪐 Vedic Astro-Tech Forecast Dashboard")


# --- User Input for Birth Details ---
st.header("🔢 Enter Your Birth Details")

with st.form("user_birth_form"):
    name = st.text_input("Your Name", value="User")
    dob = st.date_input("Date of Birth", datetime.date(1984, 9, 12))
    hour = st.number_input("Hour (0–23)", min_value=0, max_value=23, value=2)
minute = st.number_input("Minute (0–59)", min_value=0, max_value=59, value=40)
tob = datetime.time(hour, minute)
    lat = st.number_input("Latitude", value=25.45)
    lon = st.number_input("Longitude", value=81.84)
    tz = st.number_input("Time Zone (e.g. 5.5 for IST)", value=5.5)
    submitted = st.form_submit_button("Generate My Forecast")

if submitted:
    dt = datetime.datetime.combine(dob, tob)
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0) - tz / 24.0
    st.success(f"Forecast generated for {name}")
    st.session_state['jd'] = jd
    st.session_state['birth_year'] = dob.year
    st.session_state['name'] = name
    st.session_state['tz'] = tz
else:
    st.warning("Please fill your details above and click 'Generate My Forecast' to continue.")
    st.stop()


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

# --- Vimshottari Dasha Placeholder ---
st.header("🔄 Vimshottari Dasha (Coming Soon)")
st.info("This section will calculate and display your Dasha periods based on Moon Nakshatra.")

# --- Real-Time Planetary Transits Placeholder ---
st.header("🪐 Current Planetary Transits (Coming Soon)")
st.info("This will show current sidereal planetary positions relative to your Ascendant.")

# --- Gun Milan Compatibility Scoring Placeholder ---
st.header("💖 Gun Milan Score (Coming Soon)")
st.info("This will analyze Moon Nakshatra matches and provide a compatibility score out of 36.")

# --- Vimshottari Dasha Timeline ---
import swisseph as swe

st.header("🔄 Vimshottari Dasha")

def calculate_dasha_from_moon(jd_birth, birth_year):
    dasha_sequence = [
        ("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7),
        ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)
    ]
    nakshatra_lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
                       "Jupiter", "Saturn", "Mercury"] * 3
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    moon_pos, _ = swe.calc_ut(jd_birth, swe.MOON)
    ayanamsa = swe.get_ayanamsa_ut(jd_birth)
    sidereal_moon = (moon_pos[0] - ayanamsa) % 360
    nakshatra_index = int(sidereal_moon // (13 + 1/3))
    dasha_lord = nakshatra_lords[nakshatra_index]
    start_index = [i for i, (p, _) in enumerate(dasha_sequence) if p == dasha_lord][0]
    timeline = []
    current_year = birth_year
    for planet, years in dasha_sequence[start_index:] + dasha_sequence[:start_index]:
        timeline.append((planet, current_year, current_year + years))
        current_year += years
        if len(timeline) >= 6:
            break
    return timeline

dt = datetime.datetime.combine(dob, tob)
birth_dt = dt
tz = st.session_state.get('tz', 5.5)
jd = st.session_state.get('jd', swe.julday(birth_dt.year, birth_dt.month, birth_dt.day,
                birth_dt.hour + birth_dt.minute / 60.0) - tz / 24.0)

dasha_data = calculate_dasha_from_moon(st.session_state['jd'], st.session_state['birth_year'])
for planet, start, end in dasha_data:
    st.write(f"**{planet}**: {start} → {end}")

# --- Real-Time Planetary Transits ---
st.header("🌐 Current Planetary Transits (Sidereal)")

signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

def get_transits(jd_now, lagna_sign):
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    planets = [
        (swe.SUN, "Sun"), (swe.MOON, "Moon"), (swe.MERCURY, "Mercury"),
        (swe.VENUS, "Venus"), (swe.MARS, "Mars"), (swe.JUPITER, "Jupiter"),
        (swe.SATURN, "Saturn"), (swe.TRUE_NODE, "Rahu")
    ]
    transits = []
    ayanamsa = swe.get_ayanamsa_ut(jd_now)
    for pid, name in planets:
        pos, _ = swe.calc_ut(jd_now, pid)
        sidereal_lon = (pos[0] - ayanamsa) % 360
        sign_index = int(sidereal_lon // 30)
        degree = sidereal_lon % 30
        house = ((sign_index - lagna_sign + 12) % 12) + 1
        transits.append((name, signs[sign_index], degree, house))
    return transits

# Assume Lagna is Cancer (index 3)
jd_now = swe.julday(datetime.datetime.utcnow().year, datetime.datetime.utcnow().month,
                    datetime.datetime.utcnow().day)
lagna_index = 3  # Cancer Lagna
planet_data = get_transits(jd_now, lagna_index)

st.write("Lagna (Ascendant) assumed: **Cancer**")
st.table({ "Planet": [p[0] for p in planet_data],
            "Sign": [p[1] for p in planet_data],
            "Degree": [f"{p[2]:.2f}" for p in planet_data],
            "House": [p[3] for p in planet_data] })

# --- Gun Milan Compatibility Scoring ---
st.header("💖 Gun Milan Compatibility Scoring")

def get_nakshatra_index(jd):
    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    sidereal_moon = (moon_pos[0] - ayanamsa) % 360
    return int(sidereal_moon // (13 + 1/3))

with st.form("gun_milan_form"):
    st.subheader("Person 1 Details")
    dob1 = st.date_input("Date of Birth 1", datetime.date(1990, 1, 1), key="dob1")
    tob1 = st.time_input("Time of Birth 1", datetime.time(10, 0), key="tob1")
    tz1 = st.number_input("Timezone 1", value=5.5, key="tz1")

    st.subheader("Person 2 Details")
    dob2 = st.date_input("Date of Birth 2", datetime.date(1992, 2, 2), key="dob2")
    tob2 = st.time_input("Time of Birth 2", datetime.time(12, 0), key="tob2")
    tz2 = st.number_input("Timezone 2", value=5.5, key="tz2")

    submit_compat = st.form_submit_button("Check Compatibility")

if submit_compat:
    dt1 = datetime.datetime.combine(dob1, tob1)
    dt2 = datetime.datetime.combine(dob2, tob2)
    jd1 = swe.julday(dt1.year, dt1.month, dt1.day, dt1.hour + dt1.minute / 60) - tz1 / 24
    jd2 = swe.julday(dt2.year, dt2.month, dt2.day, dt2.hour + dt2.minute / 60) - tz2 / 24

    n1 = get_nakshatra_index(jd1)
    n2 = get_nakshatra_index(jd2)
    distance = abs(n1 - n2)
    max_distance = 27
    gun_score = round((36 - (distance * 1.3)), 2)
    gun_score = max(0, min(36, gun_score))  # Bound the score

    st.write(f"Moon Nakshatra Index 1: {n1}")
    st.write(f"Moon Nakshatra Index 2: {n2}")
    st.subheader(f"💑 Gun Milan Score: {gun_score} / 36")

    if gun_score >= 30:
        st.success("✅ Excellent match!")
    elif gun_score >= 24:
        st.info("👍 Good match.")
    elif gun_score >= 18:
        st.warning("⚠️ Caution advised.")
    else:
        st.error("❌ Poor compatibility.")