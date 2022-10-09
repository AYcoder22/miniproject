
import streamlit as st
import pandas as pd


year = st.slider('choose year?', 1800, 2022, 1999)
st.write("This Map Represents year:  ", year)
