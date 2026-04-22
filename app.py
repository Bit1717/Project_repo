import streamlit as st
from Feature_01 import return_even

original_list = [i for i in range(10)]

even_list = return_even(original_list)

st.set_page_config(
    page_title="FridgeBoss", 
    layout="wide"
)

st.write("Hooray, we connected everything")

st.write(even_list)
