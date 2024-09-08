import streamlit as st
from src.domain.models import Farmer, Farm, Culture
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards


selected_farmer = st.selectbox('Escolha um Produtor', options=Farmer.get_farmer_select_box_options())


if selected_farmer == 'Todos':
    farmer_id = None
else:
    farmer_id = selected_farmer.split('-')[0]

amount_col, area_col = st.columns(2)

with amount_col:
    st.metric(label="Total de Fazendas", value=Farm.get_farm_count(farmer_id))
    style_metric_cards()

with area_col:
    st.metric(label='Area Total das Fazendas (ha)', value=Farm.get_farm_total_area(farmer_id))
    style_metric_cards()

result_state = Farm.get_farm_group_by_state(farmer_id)
if result_state:
    pie_state, state_ax = plt.subplots()
    state_ax.pie(result_state.values(), labels=result_state.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
    st.pyplot(pie_state)


result_culture = Culture.get_farm_group_by_culture(farmer_id)
if result_culture:
    pie_state, state_ax = plt.subplots()
    state_ax.pie(result_culture.values(), labels=result_culture.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
    st.pyplot(pie_state)


result = Farm.get_farm_group_by_soil_use(farmer_id)

if result:
    pie_state, state_ax = plt.subplots()
    state_ax.pie(result.values(), labels=result.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
    st.pyplot(pie_state)
