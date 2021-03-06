from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris
from astropy.coordinates import EarthLocation
from astropy.coordinates import get_body
from astropy.coordinates import AltAz
from astropy import units as u
from datetime import datetime, timedelta, date
import calendar
import streamlit as st
import pandas as pd

# Porto Alegre
lat = -30.032829
lon = -51.230190
height = 0
cal = calendar.Calendar()
venus_date = []
venus_elev = []
venus_data = []

# A biblioteca dá pau com scale = "local"
for month in range(1, 13):
    monthdays = [d for d in cal.itermonthdays(2021, month) if d != 0]
    for day in monthdays:
        t = Time(datetime(2021, month, day, 1, 0, 0, 1), scale="utc", format="datetime")
        date_brazil = datetime(2021, month, day, 1, 0, 0, 1) - timedelta(hours=3)
        observation_date = date.strftime(date_brazil, "%F")
        loc = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=height * u.m)
        with solar_system_ephemeris.set('jpl'):
            venus = get_body('venus', t, loc)
        altazframe = AltAz(obstime=t, location=loc, pressure=0)
        venusaz = venus.transform_to(altazframe)
        venus_date.append(observation_date)
        venus_elev.append(str(venusaz.alt.degree))
        venus_data.append({
            "date": observation_date,
            "elevation": venusaz.alt.degree
        })

venus_csv = pd.DataFrame(venus_data)
venus_csv = venus_csv.rename(columns={'date': 'index'}).set_index('index')

st.line_chart(venus_csv)
