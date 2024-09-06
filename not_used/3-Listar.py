import time
from src.adapters.pages_models.st_farmer_model import update
import streamlit as st
from src.domain.models import Farmer


with open('src/adapters/static/css/main.css') as file:
    st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

for farmer in Farmer.select():
    if st.query_params.get('update'):
        update()
    else:
        name_col, alter_button_col, delete_button_col = st.columns(3)
        with name_col:
            st.write(f':blue[{farmer.name}]')
        with alter_button_col:
            alter_button = st.button(label='Alterar', key=f'update{farmer.name}')
        with delete_button_col:
            delete_button = st.button(label='Excluir', key=f'delete{farmer.name}')

        if alter_button:
            st.query_params['id'] = farmer.document
            st.query_params['update'] = True
            time.sleep(0.1)
            break
        if delete_button:
            farmer.delete().where(Farmer.document == farmer.document).execute()
            st.success('Exlcuído com Sucesso')
            st.query_params.clear()
            time.sleep(1)
            st.rerun()
