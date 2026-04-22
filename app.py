import streamlit as st
from Feature_01 import return_even
from Feature_02 import return_odd

st.set_page_config(
    page_title="FridgeBoss", 
    layout="wide")

#Titel + introduction
st.title("Hallo bei FridgeBoss")

st.subheader("Namen angeben")
name = st.text_input("Bitte Namen eingeben", placeholder= "Dein name ist...")
if name != "":
    st.write(f"Hallo bei FridgeBoss {name}! Ich bin dein persönliches Rezept generiersystem, wie kann ich behilflich sein")




original_list = [i for i in range(10)]

even_list = return_even(original_list)

odd_list = return_odd(original_list)

st.write("Hooray, we connected everything")

st.write(even_list)

st.write(odd_list)

