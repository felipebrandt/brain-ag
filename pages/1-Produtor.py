import streamlit as st
from src.adapters.pages_models.st_farmer_model import update, insert, search, manage


with open('src/adapters/static/css/main.css') as file:
    st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

label_has_validation_col, toggle_col = st.columns(2, vertical_alignment="center")

with label_has_validation_col:
    st.write('Ativar Validação de CPF/CNPJ')

with toggle_col:
    has_validation = st.toggle('has_validation', label_visibility='hidden')

if st.query_params.get('update'):
    update(has_validation)
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
        insert(has_validation)


