
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import os
import sqlalchemy as sa
import aggrid_option



themetemplate = 'alpine'

st.title("メインページ")

col1, col2 = st.columns([20,10])
with col1:
    st.subheader('【出荷件数チェック】')
    st.text(f'日々の出荷データ件数を集計出来ます。\n旧商品が含まれている場合、含まれている旧商品情報を表示させます。')

    st.subheader('【商品別個数集計】')
    st.text(f'日々の出荷データ内の商品別個数を集計出来ます。')


with col2:
    uploaded_file  = st.file_uploader('旧商品ファイルアップロード', type='csv')
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.to_csv('OldItem.csv')