import pandas as pd
import streamlit as st
import sqlalchemy as sa

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

import main_app
import aggrid_option
import export
import datetime


# ---Page Top
# ---st.set_page_config(page_title="ShipItem check", layout="wide") 
title = '商品別出荷数チェック'
st.title(title)
st.subheader('対象リスト')


# ---Get Data
# shows,sql_body = exec_sql.page_201_01()

uploaded_file  = st.file_uploader('ファイルアップロード', type='txt')

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='cp932', header=None, usecols=[11, 12, 14], names=('出荷依頼日', '商品コード', '件数'))
    shows = df[['出荷依頼日', '商品コード', '件数']].groupby(['出荷依頼日', '商品コード'], sort=True).sum('件数')
    st.dataframe(shows, 400, 400)
    

    # ---Export
    now = datetime.datetime.now()
    dt_now = now.strftime('%Y%m%d_%H%M%S')
    col1, col2 = st.columns([4,30])
    with col1:
        csv = export.create_csv(shows)

        st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f'{dt_now}_{title}.csv',
        mime='text/csv',
    )

    with col2:
        df_xlsx = export.to_excel(shows)
        
        st.download_button(
        label='Download EXCEL',
        data=df_xlsx ,
        file_name= f'{dt_now}_{title}.xlsx'
    )

