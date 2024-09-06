import datetime
import time

import streamlit as st
from src.domain.models import Farmer, Farm, Culture, CultureType
import re


def update():
    farm = Farm.select().where(Farm.name == st.query_params['farm_name']).get()

    culture_values_set = set()
    agricultural_area = vegetation_area = 0.0
    name_col, owner_col = st.columns(2)

    with name_col:
        name = st.text_input(label='name',
                             placeholder='Digite o nome da Fazenda...',
                             value=farm.name,
                             label_visibility='hidden')

    with owner_col:
        raw_document = st.text_input(label='document',
                                     placeholder='Digite o CPF/CNPJ do Produtor',
                                     value=farm.farmer_owner,
                                     label_visibility='hidden')
    city_col, state_col = st.columns(2)
    with city_col:
        city = st.text_input(label='city',
                             placeholder='Digite a Cidade da Fazenda...',
                             value=farm.city,
                             label_visibility='hidden')
    with state_col:
        state = st.text_input(label='state',
                              placeholder='Digite o Estado (UF) da Fazenda...',
                              value=farm.state,
                              label_visibility='hidden')

    label_area_col, box_area_col = st.columns(2)
    with label_area_col:
        st.write('Area Total')
    with box_area_col:
        area = st.number_input(label='area',
                               placeholder='Insira a Área Total da Fazenda...',
                               min_value=0.1,
                               value=farm.total_area,
                               label_visibility='hidden')

    label_last_agricultural, value_last_agricultural = st.columns(2)
    with label_last_agricultural:
        st.write(f':blue[Área Agricultável Atual:]')
    with value_last_agricultural:
        st.write(f':blue[***{farm.agricultural_area}***]')

    label_last_vegetation, value_last_vegetation = st.columns(2)
    with label_last_vegetation:
        st.write(f':blue[Área de Vegetação Atual:]')
    with value_last_vegetation:
        st.write(f':blue[***{farm.vegetation_area}***]')

    if area:
        label_agricultural_col, slide_agricultural_col = st.columns(2)
        with label_agricultural_col:
            st.write('Área Agricultável')

        with slide_agricultural_col:
            agricultural_area = st.slider('Area Agricultável Nova',
                                          min_value=0.0,
                                          max_value=area,
                                          label_visibility='hidden')
        if agricultural_area > 0 and agricultural_area != area:
            label_vegetation_col, slide_vegetation_col = st.columns(2)
            with label_vegetation_col:
                st.write('Área de Vegetação')

            with slide_vegetation_col:
                vegetation_area = st.slider('Area de Vegetação Nova',
                                            min_value=0.0,
                                            max_value=area - agricultural_area,
                                            label_visibility='hidden')
        elif agricultural_area != area:
            label_vegetation_col, slide_vegetation_col = st.columns(2)
            with label_vegetation_col:
                st.write('Área de Vegetação')

            with slide_vegetation_col:
                vegetation_area = st.slider('Area de Vegetação Nova',
                                            min_value=0.0,
                                            max_value=area,
                                            label_visibility='hidden')

    if 'culture_amount' not in st.session_state:
        st.session_state.culture_amount = 1

    label_col, culture_col, delete_culture_col = st.columns(3)

    with label_col:
        st.write('Selecione uma Cutura')
    with culture_col:
        selected_culture = st.selectbox('Selecione uma Cutura',
                                        options=Culture.get_farm_culture(farm.farm_id),
                                        label_visibility='hidden')
    with delete_culture_col:
        delete_button = st.button('Excluir Cultura', key='delete')

    if delete_button:
        Culture.delete().where(Culture.culture_type == selected_culture).execute()
        st.success('Cultura Excluida com Sucesso')
        time.sleep(1)
        st.rerun()

    label_col_culture, add_col, decrease_col = st.columns(3)
    with label_col_culture:
        st.write('Inserir/Excluir Nova Cultura:')
    with add_col:
        add_new_culture = st.button(label='➕', key='new_culture')
    with decrease_col:
        decrease_culture = st.button(label='➖', key='decrease_culture')

    if add_new_culture:
        st.session_state.culture_amount += 1

    if decrease_culture and st.session_state.culture_amount:
        st.session_state.culture_amount -= 1

    for culture in range(st.session_state.culture_amount):
        label_new_col, new_culture_col = st.columns(2)
        with label_new_col:
            st.write('Selecione a Cultura da Fazenda:')

        with new_culture_col:
            culture_value = st.selectbox('Selecione a Cultura da Fazenda:',
                                         options=CultureType.get_cultures_tuple(),
                                         key=f'culture_{culture}',
                                         label_visibility='hidden')
        culture_values_set.add(culture_value)

    update_button = st.button(label='Salvar')
    if len(state) > 2:
        st.error('Digite apenas a UF do Estado')

    if vegetation_area or agricultural_area:
        if vegetation_area + agricultural_area < area:
            st.warning(f'Sobrando {area - vegetation_area - agricultural_area} ha para distribuir')

    if raw_document:
        document = re.sub('[^0-9]', '', raw_document)
        farmer = Farmer.get_farmer(document)
        if farmer:
            if update_button:
                if name and area and city and len(state) == 2:
                    farm.name = name
                    farm.farmer_owner = document
                    farm.total_area = area
                    if agricultural_area or vegetation_area:
                        farm.agricultural_area = agricultural_area
                        farm.vegetation_area = vegetation_area
                    farm.city = city
                    farm.state = state
                    farm.update_model()
                    saved_culture_list = Culture.get_farm_culture(farm.farm_id)
                    for culture_to_save in culture_values_set:
                        if culture_to_save not in saved_culture_list:
                            Culture().create(farm=farm.farm_id,
                                             culture_type=culture_to_save,
                                             created_at=datetime.datetime.now())
                    st.query_params['id'] = document
                    st.success(f'Fazenda ***{name}*** Salva com Sucesso')
                    st.session_state.culture_amount = 1
                    time.sleep(1.5)
                    st.switch_page('main.py')

        else:
            st.warning("Produtor não Encontrado")


def insert():
    culture_values_set = set()
    agricultural_area = vegetation_area = 0.0
    name_col, owner_col = st.columns(2)

    with name_col:
        name = st.text_input(label='name',
                             placeholder='Digite o nome da Fazenda...',
                             label_visibility='hidden')

    with owner_col:
        raw_document = st.text_input(label='document',
                                     placeholder='Digite o CPF/CNPJ do Produtor',
                                     label_visibility='hidden')
    city_col, state_col = st.columns(2)
    with city_col:
        city = st.text_input(label='city',
                             placeholder='Digite a Cidade da Fazenda...',
                             label_visibility='hidden')
    with state_col:
        state = st.text_input(label='state',
                             placeholder='Digite o Estado (UF) da Fazenda...',
                             label_visibility='hidden')

    label_area_col, box_area_col = st.columns(2)
    with label_area_col:
        st.write('Area Total')
    with box_area_col:
        area = st.number_input(label='area',
                               placeholder='Insira a Área Total da Fazenda...',
                               min_value=0.1,
                               label_visibility='hidden')

    has_farm_saved = Farm.has_farm(name)
    if has_farm_saved:
        st.error(f'Já existe uma fazenda com este nome: ***{name}***')

    if area:
        label_agricultural_col, slide_agricultural_col = st.columns(2)
        with label_agricultural_col:
            st.write('Área Agricultável')

        with slide_agricultural_col:
            agricultural_area = st.slider('Area Agricultável Nova',
                                          min_value=0.0,
                                          max_value=area,
                                          label_visibility='hidden')
        if agricultural_area > 0 and agricultural_area != area:
            label_vegetation_col, slide_vegetation_col = st.columns(2)
            with label_vegetation_col:
                st.write('Área de Vegetação')

            with slide_vegetation_col:
                vegetation_area = st.slider('Area de Vegetação Nova',
                                            min_value=0.0,
                                            max_value=area-agricultural_area,
                                            label_visibility='hidden')
        elif agricultural_area != area:
            label_vegetation_col, slide_vegetation_col = st.columns(2)
            with label_vegetation_col:
                st.write('Área de Vegetação')

            with slide_vegetation_col:
                vegetation_area = st.slider('Area de Vegetação Nova',
                                            min_value=0.0,
                                            max_value=area,
                                            label_visibility='hidden')

    if 'culture_amount' not in st.session_state:
        st.session_state.culture_amount = 1

    label_col_culture, add_col, decrease_col = st.columns(3)
    with label_col_culture:
        st.write('Inserir/Excluir Nova Cultura:')
    with add_col:
        add_new_culture = st.button(label='➕', key='new_culture')
    with decrease_col:
        decrease_culture = st.button(label='➖', key='decrease_culture')

    if add_new_culture:
        st.session_state.culture_amount += 1

    if decrease_culture and st.session_state.culture_amount:
        st.session_state.culture_amount -= 1

    for culture in range(st.session_state.culture_amount):
        label_new_col, new_culture_col = st.columns(2)
        with label_new_col:
            st.write('Selecione a Cultura da Fazenda:')

        with new_culture_col:
            culture_value = st.selectbox('Selecione a Cultura da Fazenda:',
                                         options=CultureType.get_cultures_tuple(),
                                         key=f'culture_{culture}',
                                         label_visibility='hidden')
        culture_values_set.add(culture_value)

    insert_button = st.button(label='Salvar')
    if len(state) > 2:
        st.error('Digite apenas a UF do Estado')
    if vegetation_area + agricultural_area < area:
        st.warning(f'Sobrando {area - vegetation_area - agricultural_area} ha para distribuir')

    if raw_document:
        document = re.sub('[^0-9]', '', raw_document)
        farmer_list = Farmer.get_farmer(document)
        farmer = farmer_list.pop()
        if farmer:
            st.success(f"Produtor Encontrado: ***{farmer.name}***")
            if insert_button:
                if name and area and city and len(state) == 2 and not has_farm_saved:
                    new_farm = Farm().create_new(name=name,
                                                 farmer_owner=document,
                                                 total_area=area,
                                                 agricultural_area=agricultural_area,
                                                 vegetation_area=vegetation_area,
                                                 city=city,
                                                 state=state,
                                                 created_at=datetime.datetime.now())
                    for culture_to_save in culture_values_set:
                        Culture().create(farm=new_farm,
                                         culture_type=culture_to_save,
                                         created_at=datetime.datetime.now())
                    st.query_params['id'] = document
                    st.success(f'Fazenda ***{name}*** Salva com Sucesso')
                    st.session_state.culture_amount = 1
                    time.sleep(1.5)
                    st.switch_page('main.py')
                else:
                    st.error('Falta inserir dados importantes: Nome, Area Total, Cidade, Estado')

        else:
            st.warning("Produtor não Encontrado")


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
                    st.session_state.role = '2-Fazenda'
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
            name_col, select_box_col, delete_button_col, update_button_col = st.columns(4)
            farmer = has_farmer.get()

            with name_col:
                st.write(f':blue[{farmer.name}]')
            with select_box_col:
                farm_select_box = st.selectbox('Selecione uma Fazenda', options=Farm.get_farms_tuple(farmer_id))
            with delete_button_col:
                delete_button = st.button(label='Excluir', key=f'delete')
            with update_button_col:
                update_button = st.button(label='Alterar', key=f'update')

            if update_button:
                st.query_params['update'] = True
                st.query_params['farm_name'] = farm_select_box
                time.sleep(0.1)
                st.rerun()
            if delete_button:
                Farm.delete().where(Farm.name == farm_select_box).execute()
                st.success('Exlcuído com Sucesso')
                st.query_params.clear()
                time.sleep(1)
                st.switch_page('pages/2-Fazenda.py')

