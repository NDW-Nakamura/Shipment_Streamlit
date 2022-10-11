import pandas as pd
from sqlalchemy import true
import streamlit as st
from pyxlsb import open_workbook as open_xlsb
from io import BytesIO

"""
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('cp932')
"""

def create_csv(df):
    csv = df.to_csv().encode('cp932')
    return csv


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=true, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data