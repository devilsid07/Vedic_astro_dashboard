import streamlit as st
import swisseph as swe
import datetime

swe.set_ephe_path('.')  # Streamlit Cloud will use default bundled ephemeris

birth_date = datetime.datetime(1984, 9, 12, 2, 40)
birth_place = {'lat': 25.45, 'lon': 81.84, 'tz': 5.5}

def calculate_julian_day(birth_date, tz_offset):
    utc_hour = birth_date.hour + birth_date.minute / 60.0
    jd = swe.julday(birth_date.year, birth_date.month, birth_date.day, utc_hour)
    return jd - tz_offset / 24.0

def get_planetary_positions(jd):
    planets = [
        (swe.SUN, "Sun"),
        (swe.MOON, "Moon"),
        (swe.MERCURY, "Mercury"),
        (swe.VENUS, "Venus"),
        (swe.MARS, "Mars"),
        (swe.JUPITER, "Jupiter"),
        (swe.SATURN, "Saturn"),
        (swe.TRUE_NODE, "Rahu")
    ]
    results = []
    for pid, name in planets:
        pos, _ = swe.calc_ut(jd, pid)
        lon = pos[0]
        is_retro = pos[3] < 0
        results.append((name, lon, is_retro))
    return results

st.title("🪐 Vedic Astro-Tech Forecast Dashboard")

st.header("📅 Birth Chart Overview")
st.write(f"**Date:** {birth_date.strftime('%d %B %Y')}")
st.write(f"**Time:** {birth_date.strftime('%I:%M %p')}")
st.write("**Location:** Allahabad, India")

jd = calculate_julian_day(birth_date, birth_place['tz'])

st.subheader("🪐 Planetary Positions at Birth")
for name, lon, is_retro in get_planetary_positions(jd):
    st.write(f"{name}: {lon:.2f}° {'(R)' if is_retro else ''}")

st.header("🔄 Vimshottari Dasha")
st.info("Dasha calculation module coming soon...")

st.header("🌠 Transit Forecast")
st.info("Transit analysis based on current positions and your chart coming soon...")
