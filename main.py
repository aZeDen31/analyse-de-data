import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Analyse de la Pollution en Inde", layout="wide")
st.title("📊 Taux de Pollution en Inde - Analyse AQI")
st.markdown("---")
st.markdown("""
**Données source :** all_india_districts_aqi.csv

Analyse complète du **taux de pollution atmosphérique** en Inde par état et district.
Visualisation de l'**Air Quality Index (AQI)** et des principales sources de pollution.
""")
st.markdown("---")

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

# Checkboxes pour afficher/masquer les graphiques
st.sidebar.header("Affichage des graphiques")
show_bar_chart = st.sidebar.checkbox("📊 Graphique en barres", value=True)
show_time_chart = st.sidebar.checkbox("📈 Évolution de la pollution", value=True)
show_pie_chart = st.sidebar.checkbox("🥧 Répartition par source", value=True)

filtered_AQI = stateAQI[selected_states]


# --------------------------------------------------------------------------
### BAR CHART
# --------------------------------------------------------------------------
if show_bar_chart:
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
### POLLUTION OVER TIME (Most AQI vs Current AQI)
# --------------------------------------------------------------------------
if show_time_chart:
    filtered_time_df = df[df["State"].isin(selected_states)]
    time_data = filtered_time_df.groupby("State").agg({
        "Most AQI Reached": "mean",
        "Current AQI": "mean"
    }).loc[selected_states]

    figTime, axTime = plt.subplots(figsize=(12, 6))

    x_pos = range(len(time_data))
    width = 0.35

    bars1 = axTime.bar([i - width/2 for i in x_pos], time_data["Most AQI Reached"], width, label='Max AQI Atteint', color='#FF6B6B', alpha=0.8)
    bars2 = axTime.bar([i + width/2 for i in x_pos], time_data["Current AQI"], width, label='AQI Actuel', color='#4ECDC4', alpha=0.8)

    axTime.set_xlabel("État", color='white')
    axTime.set_ylabel("Valeur AQI", color='white')
    axTime.set_title("Évolution de la Pollution : AQI Max vs AQI Actuel", color='white')
    axTime.set_xticks(x_pos)
    axTime.set_xticklabels(time_data.index, rotation=45, ha='right')
    axTime.legend(loc='upper right', facecolor='#1a1a1a', edgecolor='white', labelcolor='white')

    figTime.patch.set_alpha(0)
    axTime.set_facecolor('none')
    axTime.tick_params(colors='white')
    axTime.spines['bottom'].set_color('white')
    axTime.spines['left'].set_color('white')
    axTime.spines['top'].set_color('none')
    axTime.spines['right'].set_color('none')
    axTime.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.3, axis='y')
    axTime.set_axisbelow(True)

    st.pyplot(figTime)

# --------------------------------------------------------------------------
### CAMEMBERT
# --------------------------------------------------------------------------
if show_pie_chart:
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

