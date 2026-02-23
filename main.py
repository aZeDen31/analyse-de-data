import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.write("Streamlit Demo")
df = pd.read_csv('all_india_districts_aqi.csv')
stateAQI = df.groupby("State")["Current AQI"].sum()
stateAQI = stateAQI.sort_values(ascending=False)

# Sidebar pour sélectionner les états
st.sidebar.header("Filtres")
all_states = stateAQI.index.tolist()
selected_states = st.sidebar.multiselect(
    "Choisir les états à afficher",
    options=all_states,
    default=all_states
)

filtered_AQI = stateAQI[selected_states]


# --------------------------------------------------------------------------
### BAR CHART
# --------------------------------------------------------------------------
figBar, axBar = plt.subplots(figsize=(12, 6))
axBar.bar(filtered_AQI.index, filtered_AQI.values, color='skyblue')
axBar.set_xlabel("State", color='white')
axBar.set_ylabel("Current AQI", color='white')
axBar.set_title("AQI par État (India)", color='white')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
figBar.patch.set_alpha(0)
axBar.set_facecolor('none')
axBar.tick_params(colors='white')
axBar.spines['bottom'].set_color('white')
axBar.spines['left'].set_color('white')
axBar.spines['top'].set_color('none')
axBar.spines['right'].set_color('none')
axBar.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.3)
axBar.set_axisbelow(True)

st.pyplot(figBar)

# --------------------------------------------------------------------------
### CAMEMBERT
# --------------------------------------------------------------------------
traduction = {
    'Vehicle': 'Véhicules',
    'Industrial Emissions': 'Émissions industrielles',
    'Road Dust': 'Poussière de route',
    'Domestic Fuel': 'Combustible domestique',
    'Crop Burning': 'Brûlage de cultures',
    'Construction Dust': 'Poussière de construction',
    'Waste Burning': 'Brûlage de déchets'
}

df['Source FR'] = df['Major Source of Pollution'].map(traduction)

filtered_df = df[df["State"].isin(selected_states)]
pollution_counts = filtered_df["Source FR"].value_counts()

figCam, axCam = plt.subplots(figsize=(8, 8))
explode = [0.03] * len(pollution_counts)
axCam.pie(pollution_counts.values, labels=pollution_counts.index, autopct='%1.1f%%', startangle=90, textprops={'color':"white"}, explode=explode)

axCam.set_title("Répartition des sources de pollution", color='white')
figCam.patch.set_alpha(0)

st.pyplot(figCam)

