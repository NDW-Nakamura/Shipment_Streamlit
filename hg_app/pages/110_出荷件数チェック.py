import pandas as pd
import streamlit as st
import sqlalchemy as sa
from PIL import Image

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

import main_app
import aggrid_option
import export
import datetime


# ---Page Top
st.set_page_config(page_title="ShipRecord check", layout="wide") 
title = '出荷ファイル受注件数チェック'
st.title(title)
st.subheader('対象リスト')


# ---Get Data
# shows,sql_body = exec_sql.page_201_01()

uploaded_file  = st.file_uploader('ファイルアップロード', type='txt')

if uploaded_file:
    df = pd.read_csv(uploaded_file
                    , encoding='cp932'
                    , header=None
                    , usecols=[0, 11, 12, 14]
                    , names=('受注番号', '出荷依頼日', '商品コード', '明細数')
                    , dtype={"受注番号": object
                            ,"商品コード":object})
                            
    shows = df[['出荷依頼日', '受注番号', '明細数']].groupby(['出荷依頼日', '受注番号'], sort=True).sum('明細数')
    st.subheader(f'出荷データ件数：{len(shows)}件')
    col1, col2,col3 = st.columns([8,8,12])
    with col1:
        st.text('受注番号で集計、右端の数字は明細行数')
        st.dataframe(shows, 800, 300)
    with col2:
        st.text('旧商品が入っていると↓に表示されます。') 
        olditemdf = pd.read_csv('OldItem.csv', usecols=[1], dtype=object)
        targetitem = olditemdf['HG-ID'].to_list()
        shows2 = (df[df['商品コード'].isin(targetitem)])
        st.dataframe(shows2)
    with col3:       
        if len(shows2) > 0:
            st.text('旧商品一覧。')
            df = pd.read_csv('OldItem.csv'
                        , usecols=[0, 1, 2])
            st.dataframe(df)

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




if "count" not in st.session_state: # (C)
        st.session_state.count = 1 # (A)
    
increment = st.button("使い方を見る") # (B)
if increment:
    st.session_state.count += 1 # (A)

if st.session_state.count % 2 == 0:
    image = Image.open('main\\hg_app\\image\\1.png')
    st.image(image)

    image2 = Image.open('main\\hg_app\\image\\1.png')
    st.image(image2)
