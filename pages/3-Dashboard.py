import streamlit as st
from src.domain.models import Farm, Culture
import matplotlib.pyplot as plt


amount_col, pie_state_col = st.columns(2)

with amount_col:
    st.title(Farm.get_farm_count())

with pie_state_col:
    result = Farm.get_farm_group_by_state()
    pie_state, state_ax = plt.subplots()
    state_ax.pie(result.values(), labels=result.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
    state_ax.axis('equal')
    st.pyplot(pie_state)

pie_culture_col, pie_soil_use_col = st.columns(2)
with pie_culture_col:
    result = Culture.get_farm_group_by_culture()
    pie_state, state_ax = plt.subplots()
    state_ax.pie(result.values(), labels=result.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
    state_ax.axis('equal')
    st.pyplot(pie_state)

with pie_soil_use_col:
    result = Farm.get_farm_group_by_soil_use()
    pie_state, state_ax = plt.subplots()
    state_ax.pie(result.values(), labels=result.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
    state_ax.axis('equal')
    st.pyplot(pie_state)
