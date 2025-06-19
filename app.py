import streamlit as st
import swisseph as swe
import datetime

# Constants
signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
dasha_sequence = [
    ("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7),
    ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)
]

swe.set_sid_mode(swe.SIDM_LAHIRI)

# User input
st.title("🪐 Vedic Astro-Tech Forecast Dashboard")

st.sidebar.header("🧾 Enter Birth Details")
birth_date = st.sidebar.date_input("Date of Birth", datetime.date(1984, 9, 12))
birth_time = st.sidebar.time_input("Time of Birth", datetime.time(2, 40))
lat = st.sidebar.number_input("Latitude", value=25.45)
lon = st.sidebar.number_input("Longitude", value=81.84)
tz = st.sidebar.number_input("Timezone Offset", value=5.5)

# Julian Day calculation
def get_julian_day(date_obj, time_obj, tz):
    dt = datetime.datetime.combine(date_obj, time_obj)
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)
    return jd - tz / 24.0

jd = get_julian_day(birth_date, birth_time, tz)

# Planetary positions
def get_planetary_positions(jd):
    planets = [
        (swe.SUN, "Sun"), (swe.MOON, "Moon"), (swe.MERCURY, "Mercury"),
        (swe.VENUS, "Venus"), (swe.MARS, "Mars"), (swe.JUPITER, "Jupiter"),
        (swe.SATURN, "Saturn"), (swe.TRUE_NODE, "Rahu")
    ]
    ayanamsa = swe.get_ayanamsa_ut(jd)
    results = []
    for pid, name in planets:
        pos, _ = swe.calc_ut(jd, pid)
        sidereal = (pos[0] - ayanamsa) % 360
        is_retro = pos[3] < 0
        results.append((name, sidereal, is_retro))
    return results

# Ascendant (Lagna)
def get_lagna(jd, lat, lon):
    flags = swe.FLG_SIDEREAL | swe.FLG_SWIEPH
    return signs[int(swe.houses_ex(jd, lat, lon, b'A', flags)[0][0] // 30)]

# Moon sign
def get_moon_sign(jd):
    pos, _ = swe.calc_ut(jd, swe.MOON)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    sidereal_lon = (pos[0] - ayanamsa) % 360
    return signs[int(sidereal_lon // 30)]

# Vimshottari Dasha
def calculate_vimshottari_dasha(jd):
    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    sidereal_moon = (moon_pos[0] - ayanamsa) % 360
    nakshatra_index = int(sidereal_moon / (13 + 1/3))
    dasha_start_index = nakshatra_index % 9
    current_dasha = dasha_sequence[dasha_start_index:]
    dasha_timeline = []
    start_year = birth_date.year
    for planet, duration in current_dasha[:3]:
        end_year = start_year + duration
        dasha_timeline.append((planet, start_year, end_year))
        start_year = end_year
    return dasha_timeline

# Transit Analysis
def get_transit_info(jd_today, lagna_sign_index):
    planets = [
        (swe.SUN, "Sun"), (swe.MOON, "Moon"), (swe.MERCURY, "Mercury"),
        (swe.VENUS, "Venus"), (swe.MARS, "Mars"), (swe.JUPITER, "Jupiter"),
        (swe.SATURN, "Saturn"), (swe.TRUE_NODE, "Rahu")
    ]
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayanamsa = swe.get_ayanamsa_ut(jd_today)
    results = []
    for pid, name in planets:
        pos, _ = swe.calc_ut(jd_today, pid)
        sidereal = (pos[0] - ayanamsa) % 360
        sign = signs[int(sidereal // 30)]
        house = ((int(sidereal // 30) - lagna_sign_index) % 12) + 1
        results.append((name, sign, sidereal % 30, house))
    return results

# Display Info
st.header("🧭 Natal Chart Summary")
st.write("**Ascendant (Lagna):**", get_lagna(jd, lat, lon))
st.write("**Moon Sign:**", get_moon_sign(jd))

st.subheader("🪐 Planetary Positions at Birth")
for name, lon, retro in get_planetary_positions(jd):
    st.write(f"{name}: {lon:.2f}° {'(R)' if retro else ''}")

st.subheader("🔄 Vimshottari Dasha")
for planet, start, end in calculate_vimshottari_dasha(jd):
    st.write(f"{planet}: {start} - {end}")

st.subheader("🌠 7-Day Transit Forecast")
lagna = get_lagna(jd, lat, lon)
lagna_index = signs.index(lagna)
for i in range(7):
    date = datetime.datetime.utcnow() + datetime.timedelta(days=i)
    jd_day = swe.julday(date.year, date.month, date.day)
    st.write(f"**{date.strftime('%A, %d %B %Y')}**")
    for name, sign, deg, house in get_transit_info(jd_day, lagna_index):
        st.write(f"{name}: {sign} {deg:.2f}° - House {house}")

# --- Muhurta Finder ---
def find_good_muhurta(event_type):
    event_muhurta_rules = {
        "business": ["Wednesday", "Thursday", "Friday"],
        "travel": ["Monday", "Thursday"]
    }
    today = datetime.date.today()
    suggestions = []
    for i in range(14):
        future_day = today + datetime.timedelta(days=i)
        weekday = future_day.strftime("%A")
        if weekday in event_muhurta_rules.get(event_type.lower(), []):
            suggestions.append(future_day.strftime("%A, %d %B %Y"))
        if len(suggestions) >= 5:
            break
    return suggestions

# --- Hora Window Calculator (simplified version) ---
def get_day_horas(date, tz_offset):
    base = datetime.datetime.combine(date, datetime.time(6, 0))  # Assume sunrise 6 AM
    horas = []
    hora_planets = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
    weekday_index = date.weekday()
    first_lord = hora_planets[weekday_index % 7]
    sequence = hora_planets[hora_planets.index(first_lord):] + hora_planets[:hora_planets.index(first_lord)]
    for i in range(24):
        start_time = (base + datetime.timedelta(hours=i)).time()
        end_time = (base + datetime.timedelta(hours=i + 1)).time()
        planet = sequence[i % 7]
        horas.append((start_time.strftime('%H:%M'), end_time.strftime('%H:%M'), planet))
    return horas

st.header("🔍 Muhurta Finder")
event_choice = st.selectbox("Select event type", ["business", "travel"])
muhurta_list = find_good_muhurta(event_choice)
st.write("**Suggested Muhurta Dates:**")
for m in muhurta_list:
    st.write(f"✅ {m}")

st.subheader("🕐 Hora Timings for Today")
today_date = datetime.date.today()
hora_windows = get_day_horas(today_date, tz)
for start, end, planet in hora_windows:
    st.write(f"{start} - {end} → {planet} Hora")

# --- Compatibility Matching ---
def get_nakshatra_and_sign(jd):
    pos, _ = swe.calc_ut(jd, swe.MOON)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    sidereal_lon = (pos[0] - ayanamsa) % 360
    nakshatra_index = int(sidereal_lon / (13 + 1/3))
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    sign = signs[int(sidereal_lon // 30)]
    return nakshatras[nakshatra_index], sign

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
        jd1 = get_julian_day(dob1, tob1, tz1)
        jd2 = get_julian_day(dob2, tob2, tz2)
        nak1, sign1 = get_nakshatra_and_sign(jd1)
        nak2, sign2 = get_nakshatra_and_sign(jd2)

        st.write("**Person 1:**")
        st.write(f"Moon Sign: {sign1}, Nakshatra: {nak1}")
        st.write("**Person 2:**")
        st.write(f"Moon Sign: {sign2}, Nakshatra: {nak2}")
        st.success("Gun Milan Score and detailed match coming soon...")

# --- Email Notification Setup Placeholder ---
st.header("📧 Daily Email Notifications")
st.write("This feature will email your daily forecast, dasha, and muhurta.")
email = st.text_input("Enter your email address to receive daily updates:")
if st.button("Activate Email Alerts"):
    st.success(f"Email setup saved for: {email} (This is a placeholder. SMTP setup to be configured.)")