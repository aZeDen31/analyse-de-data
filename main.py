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

# boutons pour sélectionner/effacer tout rapidement
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("✔️ Tout sélectionner"):
        selected_states = all_states
with col2:
    if st.button("❌ Effacer tout"):
        selected_states = []

selected_states = st.sidebar.multiselect(
    "Choisir les états à afficher",
    options=all_states,
    default=all_states if 'selected_states' not in locals() else selected_states
)

max_states = st.sidebar.slider(
    "Nombre maximum d'états à montrer", 1, len(all_states), len(all_states)
)
selected_states = selected_states[:max_states]

st.sidebar.header("Affichage des graphiques")
show_bar_chart = st.sidebar.checkbox("📊 Graphique en barres", value=True)
show_time_chart = st.sidebar.checkbox("📈 Évolution de la pollution", value=True)
show_line_chart = st.sidebar.checkbox("📈 Courbe moyenne AQI", value=True)
show_pie_chart = st.sidebar.checkbox("🥧 Répartition par source", value=True)

filtered_AQI = stateAQI[selected_states]

filtered_time_df = df[df["State"].isin(selected_states)]
time_data = filtered_time_df.groupby("State").agg({
    "Most AQI Reached": "mean",
    "Current AQI": "mean"
}).loc[selected_states]

avg_df = time_data.copy()
avg_df = avg_df.assign(
    Moyenne_AQI=avg_df[["Most AQI Reached", "Current AQI"]].mean(axis=1),
    Ecart_Type_AQI=avg_df[["Most AQI Reached", "Current AQI"]].std(axis=1, ddof=0),
    Diff_AQI=avg_df["Most AQI Reached"] - avg_df["Current AQI"]
)

avg_df["Niveau"] = avg_df["Moyenne_AQI"].apply(
    lambda x: "Élevé" if x >= 150 else "Modéré" if x >= 100 else "Faible"
)

avg_df_display = avg_df.rename(columns={
    "Most AQI Reached": "AQI Max Atteint",
    "Current AQI": "AQI Actuel",
    "Moyenne_AQI": "Moyenne AQI",
    "Ecart_Type_AQI": "Écart-type AQI",
    "Diff_AQI": "Différence AQI"
})[["AQI Max Atteint", "AQI Actuel", "Moyenne AQI", "Écart-type AQI", "Différence AQI", "Niveau"]].round(1)

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
    figBar.patch.set_facecolor('none')
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
### LINE CHART (Moyenne AQI par État)
# --------------------------------------------------------------------------
if show_line_chart:
    figLine, axLine = plt.subplots(figsize=(12, 6))
    axLine.plot(avg_df.index, avg_df["Moyenne_AQI"], marker='o', linestyle='-', color='#FFD166')
    axLine.set_xlabel("État", color='white')
    axLine.set_ylabel("Moyenne AQI", color='white')
    axLine.set_title("Tendance de la Moyenne AQI par État", color='white')
    axLine.set_xticks(range(len(avg_df)))
    axLine.set_xticklabels(avg_df.index, rotation=45, ha='right')
    axLine.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.3, axis='y')
    figLine.patch.set_alpha(0)
    figLine.patch.set_facecolor('none')
    axLine.set_facecolor('none')
    axLine.tick_params(colors='white')
    axLine.spines['bottom'].set_color('white')
    axLine.spines['left'].set_color('white')
    axLine.spines['top'].set_color('none')
    axLine.spines['right'].set_color('none')
    axLine.set_axisbelow(True)

    st.pyplot(figLine)

# --------------------------------------------------------------------------
### TABLEAU DES MOYENNES AQI
# --------------------------------------------------------------------------
st.markdown("### 📋 Moyenne AQI par État")
st.dataframe(avg_df_display)

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

    df = df.assign(Source_FR=df['Major Source of Pollution'].map(traduction))

    filtered_df = df[df["State"].isin(selected_states)]
    pollution_counts = filtered_df["Source_FR"].value_counts()

    figCam, axCam = plt.subplots(figsize=(8, 8))
    explode = [0.03] * len(pollution_counts)
    axCam.pie(pollution_counts.values, labels=pollution_counts.index, autopct='%1.1f%%', startangle=90, textprops={'color':"white"}, explode=explode)

    axCam.set_title("Répartition des sources de pollution", color='white')
    figCam.patch.set_alpha(0)

    st.pyplot(figCam)

