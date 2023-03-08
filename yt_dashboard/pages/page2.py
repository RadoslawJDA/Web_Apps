import streamlit as st
import pandas as pd

df = pd.read_csv('D:\Documents\GitHub\Web_Apps\yt_dashboard\file.csvfile.csv')

if df:
    st.text('complete')