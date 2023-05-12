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
# ---st.set_page_config(page_title="ShipRecord check", layout="wide") 
title = '出荷ファイル受注件数チェック'
st.title(title)
st.subheader('対象リスト')

# ---Get Data
# shows,sql_body = exec_sql.page_201_01()

uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=True,key=None)
filecount = 0
filedisc_res = ''

for uploaded_f in uploaded_file:
    filecount += 1
    df = pd.read_csv(uploaded_f
                    , encoding='cp932'
                    , header=None
                    , usecols=[0, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 14]
                    , names=('受注番号', '会員氏名', '送付先名', '郵便番号', '都道府県', '市区町村', '住所１', '住所２', '住所３', '出荷依頼日', '商品コード', '明細数')
                    , dtype={"受注番号": object
                            ,"会員氏名": object
                            ,"送付先名": object
                            ,"郵便番号": object
                            ,"都道府県": object
                            ,"市区町村": object
                            ,"住所１": object
                            ,"住所２": object
                            ,"住所３": object
                            ,"商品コード": object})
    
    s = uploaded_f.name
    s_year, s_month, s_day, s_index, s_mcategory, s_memtext, s_extension = s[:4], s[4:6], s[6:8], s[8:10], s[10:11], s[11:13], s[13:]

    fn = f'<span style="font-size: 24px">{filecount}_ファイル名:</span>\
            {s_year}<span style="font-weight: bold; font-size: 48px; color:coral">{s_month}{s_day}{s_index}{s_mcategory}</span>{s_memtext}{s_extension}'
    st.write(f'{fn}', unsafe_allow_html=True)


    shows = df[['出荷依頼日', '受注番号', '明細数']].groupby(['出荷依頼日', '受注番号'], sort=True).count()
    count = len(shows)
    
    reccount = f'<span style="font-size: 24px">出荷データ件数：</span>\
            <span style="font-weight: bold; font-size: 48px; color:Teal">{count}</span>件'
    st.write(reccount, unsafe_allow_html=True)



    tabcheck = df.fillna('')

    order = (tabcheck[tabcheck['受注番号'].str.contains('\t')])
    if len(order) > 0:
        st.write(f'<span style="color:red">受注番号にタブが含まれています</span>', unsafe_allow_html=True)
        st.dataframe(order)
    
    name = (tabcheck[tabcheck['会員氏名'].str.contains('\t')])
    if len(name) > 0:
        st.write(f'<span style="color:red">会員氏名にタブが含まれています</span>', unsafe_allow_html=True)
        st.dataframe(name)

    sendname = (tabcheck[tabcheck['送付先名'].str.contains('\t')])
    if len(sendname) > 0:
        st.write(f'<span style="color:red">送付先名にタブが含まれています</span>', unsafe_allow_html=True)
        st.dataframe(sendname)

    post = (tabcheck[tabcheck['郵便番号'].str.contains('\t')])
    if len(post) > 0:
        st.write(f'<span style="color:red">郵便番号にタブが含まれています</span>', unsafe_allow_html=True)
        st.dataframe(post)

    pref = (tabcheck[tabcheck['都道府県'].str.contains('\t')])
    if len(pref) > 0:
        st.write(f'<span style="color:red">都道府県にタブが含まれています</span>', unsafe_allow_html=True)
        st.dataframe(pref)

    city = (tabcheck[tabcheck['市区町村'].str.contains('\t')])
    if len(city) > 0:
        st.write(f'<span style="color:red">市区町村にタブが含まれています</span>', unsafe_allow_html=True)
        st.dataframe(city)

    add1 = (tabcheck[tabcheck['住所１'].str.contains('\t')])
    if len(add1) > 0:
        st.write(f'<span style="color:red">住所１にタブが含まれています</span>', unsafe_allow_html=True)
        st.dataframe(add1)

    add2 = (tabcheck[tabcheck['住所２'].str.contains('\t')])
    if len(add2) > 0:
        st.write(f'<span style="color:red">住所２にタブが含まれています</span>', unsafe_allow_html=True)
        st.dataframe(add2)
    
    add3 = (tabcheck[tabcheck['住所３'].str.contains('\t')])
    if len(add3) > 0:
        st.write(f'<span style="color:red">住所３にタブが含まれています</span>', unsafe_allow_html=True)
        st.dataframe(add3)
    

    col1, col2, col3 = st.columns([8,8,12])
    with col1:
        st.text('受注番号で集計、右端の数字は明細行数')
        st.dataframe(shows, 800, 300)
        if shows['明細数'].isin([0]).any():
            print(shows['明細数'])
            errmess = f'<span style="font-weight: bold; font-size: 24px; color:coral">購入商品が無い受注が存在します。</span>'
            st.write(f'{errmess}', unsafe_allow_html=True)
    with col2:
        st.text('旧商品が入っていると↓に表示されます。')
        # olditemdf = pd.read_csv('OldItem.csv', usecols=[1], dtype=object)
        # targetitem = olditemdf['HG-ID'].to_list()
        # shows2 = (df[df['商品コード'].isin(targetitem)])
        shows2 = (df[df['商品コード'].isin(['103','105','109','111','112','113','114','115','116','117','118','119','123','124','125','126','127','128','131','148','152','153','154','155','201','217','218','220','230','231','243','247','258'])])
        st.dataframe(shows2.loc[:, ['受注番号', '会員氏名','商品コード']])
    with col3:
        if len(shows2) > 0:
            st.write(f'<span style="color:red;font-weight:bold;font-size: 48px">👈旧商品にご注意ください！！！</span>', unsafe_allow_html=True)
            st.text('旧商品一覧。')
            olditem = pd.read_csv('OldItem.csv'
                         , usecols=[1, 2])
            st.dataframe(olditem)

    st.markdown("---") #区切り線

    youbi_list = {1:"月", 2:"火", 3:"水", 4:"木", 5:"金", 6:"土", 7:"日"}
    date = datetime.date(int(s_year),int(s_month),int(s_day))
    youbi = date.isoweekday()
    youbi_txt = youbi_list[youbi]

    filedisc = (f'{s_month}月{s_day}日（{youbi_txt}）出荷データ\n「{s_year}{s_month}{s_day}{s_index}{s_mcategory}{s_memtext}」－{s_mcategory}会員様向け－（{count}件)\n')

    if s_mcategory == "B":
        filedisc = (f'{filedisc}                           ※契約書面押印日『{s_month}月{s_day}日』\n')
    
    filedisc_res = filedisc_res + filedisc

    
st.code(filedisc_res)

st.markdown("---") #区切り線

if "count" not in st.session_state: # (C)
        st.session_state.count = 1 # (A)
    
increment = st.button("使い方を見る") # (B)
if increment:
    st.session_state.count += 1 # (A)

if st.session_state.count % 2 == 0:
    image = Image.open('hg_app/image/1.png')
    st.image(image)

    image2 = Image.open('hg_app/image/3.png')
    st.image(image2)
