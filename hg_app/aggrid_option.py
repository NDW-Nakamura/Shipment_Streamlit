from pickle import FALSE
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder


def grid_option_main(gb):
    gb.configure_pagination()
    gb.configure_side_bar()
    gb.configure_selection()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
    gridOptions = gb.build()
    return gridOptions


def grid_option_simple(gb):
    gb.configure_selection()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=False)
    gridOptions = gb.build()
    return gridOptions