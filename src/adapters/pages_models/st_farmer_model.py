import time

import streamlit as st
from src.domain.models import Farmer
from src.domain.validation_utils import validate_cpf, validate_cnpj
import re


def update():
    document = st.query_params.get('id')
    has_farmer = Farmer.select().where(Farmer.document == document)
    farmer = has_farmer.get()
    input_values = farmer.get_input_values()
    with st.form(f"update_form{farmer.name}", clear_on_submit=True):
        name = st.text_input(label='name',
                             placeholder='Digite o nome do produtor...',
                             value=input_values['name'],
                             label_visibility='hidden')
        document_col, choice_col = st.columns(2)

        with choice_col:
            document_type = st.selectbox('doc_type',
                                         ('CPF', 'CNPJ'),
                                         label_visibility='hidden')

        with document_col:
            raw_document = st.text_input(label='document',
                                         placeholder='Digite o CPF/CNPJ do Produtor',
                                         value=input_values['document'],
                                         label_visibility='hidden')

        update_button = st.form_submit_button(label='Salvar')
        if update_button:
            if name:
                is_valid = False
                if document_type == 'CPF':
                    if validate_cpf(raw_document):
                        is_valid = True
                        st.success("CPF válido! ✔️")
                    else:
                        st.error("CPF inválido. ❌")
                else:
                    if validate_cnpj(raw_document):
                        is_valid = True
                        st.success("CNPJ válido! ✔️")
                    else:
                        st.error("CNPJ inválido. ❌")
                if is_valid:
                    farmer.name = name
                    farmer.document = re.sub('[^0-9]', '', raw_document)
                    farmer.document_type = document_type
                    farmer.update_model()
                    st.success(f"***{farmer.name}***: Alterado com Sucesso ✔️")
                    st.query_params.clear()
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning('Digite o Nome do Produtor')


def insert():
    with st.form("insert_form", clear_on_submit=True):
        name = st.text_input(label='name',
                             placeholder='Digite o nome do produtor...',
                             label_visibility='hidden')
        document_col, choice_col = st.columns(2)

        with choice_col:
            document_type = st.selectbox('doc_type', ('CPF', 'CNPJ'), label_visibility='hidden')
        with document_col:
            raw_document = st.text_input(label='document',
                                         placeholder='Digite o CPF/CNPJ do Produtor',
                                         label_visibility='hidden')

        insert_button = st.form_submit_button(label='Salvar')
        if insert_button:
            if name:
                is_valid = False
                document = re.sub('[^0-9]', '', raw_document)
                if not Farmer.has_farmer(document):
                    if document_type == 'CPF':
                        if validate_cpf(raw_document):
                            is_valid = True
                            st.success("CPF válido! ✔️")
                        else:
                            st.error("CPF inválido. ❌")
                    else:
                        if validate_cnpj(raw_document):
                            is_valid = True
                            st.success("CNPJ válido! ✔️")
                        else:
                            st.error("CNPJ inválido. ❌")
                    if is_valid:
                        new_farmer = Farmer().create_new(name, document, document_type)
                        st.success(f"***{new_farmer.name}***: Salvo com Sucesso ✔️")
                else:
                    st.error(f"***{document}***: Produtor Já Cadastrado️, Redirecionando...")
                    time.sleep(2)
                    st.query_params['id'] = document
                    st.session_state.role = '1-Produtor'
                    st.rerun()
            else:
                st.warning('Digite o Nome do Produtor')


def search():
    with st.form('search_form', clear_on_submit=True):
        input_col, button_col = st.columns(2)
        with input_col:
            raw_document = st.text_input(label='document',
                                         placeholder='Digite o CPF/CNPJ do Produtor',
                                         label_visibility='hidden')
        with button_col:
            search_button = st.form_submit_button(label='🔎')
        if search_button:
            if raw_document:
                document = re.sub('[^0-9]', '', raw_document)
                has_farmer = Farmer.select().where(Farmer.document == document)
                if has_farmer:
                    st.query_params['id'] = document
                    st.session_state.role = '1-Produtor'
                    st.rerun()
                else:
                    st.error(f'Produtor para o registro ***:red[{document}]*** não encontrado')

            else:
                st.error('Digite CPF/CNPJ do Produtor')


def manage():
    farmer_id = st.query_params['id']
    if farmer_id:
        st.query_params['id'] = farmer_id
        has_farmer = Farmer.select().where(Farmer.document == farmer_id)
        if has_farmer:
            farmer = has_farmer.get()
            name_col, alter_button_col, delete_button_col = st.columns(3)
            with name_col:
                st.write(f':blue[{farmer.name}]')
            with alter_button_col:
                alter_button = st.button(label='Alterar')
            with delete_button_col:
                delete_button = st.button(label='Excluir')

            if alter_button:
                st.query_params['update'] = True
                time.sleep(0.1)
                st.rerun()
            if delete_button:
                farmer.delete().where(Farmer.document == farmer_id).execute()
                st.success('Exlcuído com Sucesso')
                st.query_params.clear()
                time.sleep(1)
                st.rerun()

