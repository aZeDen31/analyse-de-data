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

# Filtrer selon la sélection
filtered_AQI = stateAQI[selected_states]

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(filtered_AQI.index, filtered_AQI.values, color='skyblue')
ax.set_xlabel("State", color='white')
ax.set_ylabel("Current AQI", color='white')
ax.set_title("AQI par État (India)", color='white')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
fig.patch.set_alpha(0)
ax.set_facecolor('none')
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.3)
ax.set_axisbelow(True)

st.pyplot(fig)