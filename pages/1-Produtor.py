import streamlit as st
from src.domain.pages_models.st_farmer_model import update, insert, search, manage

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
        ["Buscar um Produtor", "Inserir um Produtor"],
        label_visibility='hidden'
    )
    if action == "Buscar um Produtor":
        search()
    else:
        insert()


