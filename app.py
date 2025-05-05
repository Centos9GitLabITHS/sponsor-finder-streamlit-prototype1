import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("Sponsor Finder for Sports Associations")

# 1) Sample data
data = [
    {"name": "RAMSELE DATASTUGA", "postcode": "88040", "lat": 63.5884, "lon": 17.2753},
    {"name": "LINDOME GIF",        "postcode": "43700", "lat": 57.6747, "lon": 11.9336},
    {"name": "GÖTEBORG FK",       "postcode": "41502", "lat": 57.7089, "lon": 11.9746},
    {"name": "MALMÖ FF",          "postcode": "21218", "lat": 55.6050, "lon": 13.0038},
    {"name": "UPPSALA IH",        "postcode": "75310", "lat": 59.8586, "lon": 17.6389},
]
df = pd.DataFrame(data)

# 2) Sidebar filters
st.sidebar.header("Filters")
postcode = st.sidebar.text_input("Search by postal code", "")
letter   = st.sidebar.text_input("Starts with (A–Ö)", "")

filtered = df.copy()
if postcode:
    filtered = filtered[filtered["postcode"].str.contains(postcode)]
if letter:
    filtered = filtered[filtered["name"].str.upper().str.startswith(letter.upper())]

st.sidebar.markdown(f"**{len(filtered)} found**")
if postcode or letter:
    st.sidebar.dataframe(filtered[["name", "postcode"]])
else:
    st.sidebar.info("Enter a postcode or initial letter to search")

# 3) Map view
st.subheader("Map")
m = folium.Map(location=[59.3293, 18.0686], zoom_start=6)  # center on Sweden
for _, row in filtered.iterrows():
    folium.Marker([row.lat, row.lon], tooltip=row.name).add_to(m)
st_folium(m, width=700, height=400)

# 4) Registration stub
st.markdown("---")
st.header("Register your club")
st.markdown("[Click here to sign up](#)")
