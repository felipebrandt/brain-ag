from src.adapters.pages_models.st_farm_model import insert, search, update, manage
import streamlit as st

with open('src/adapters/static/css/main.css') as file:
    st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

if st.query_params.get('update'):
    update()
elif st.query_params.get('id'):
    manage()
else:
    st.title('Brain Agriculture')
    action = st.radio(
        "Radio",
        ["Buscar Fazendas", "Inserir Fazendas"],
        label_visibility='hidden'
    )
    if action == "Buscar Fazendas":
        search()
    else:
        insert()
