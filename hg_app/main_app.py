import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from bs4 import BeautifulSoup
import os
import sqlalchemy as sa
import aggrid_option
import requests

st.set_page_config(page_title="MainPage", layout="wide") 
themetemplate = 'alpine'

st.title("メインページ")

col1, col2 = st.columns([20,12])

with col1:
    st.subheader("【ヤマト運輸公式発表】最新重要ニュース")   
    r = requests.get("https://www.yamato-hd.co.jp/important/")
    soup = BeautifulSoup(r.content, "html.parser")
    
    #必要な情報のクラスを指定して抽出
    found = soup.find('div', class_='Main__content')

    style = '''
                <style>
                    time.news__date{
                        font-size: 24px;
                    }

                    h3.news__title{
                        font-size: 18px;
                    }
                </style>)'''

    # print(f'{found}{style}')
    
    found = (str(found).replace('href="/', 'href="https://www.yamato-hd.co.jp/'))
    st.write(f'{found}{style}', unsafe_allow_html=True)
    
    
with col2:
    st.subheader('【出荷件数チェック】')
    st.text(f'日々の出荷データ件数を集計出来ます。\n旧商品が含まれている場合、含まれている旧商品情報を表示させます。')

    st.subheader('【商品別個数集計】')
    st.text(f'日々の出荷データ内の商品別個数を集計出来ます。')

    st.subheader('【旧商品登録】')
    uploaded_file  = st.file_uploader('旧商品ファイルアップロード', type='csv')
    if uploaded_file:
        
        df = pd.read_csv(uploaded_file)
        # df.to_csv('OldItem.csv')
