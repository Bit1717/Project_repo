import streamlit as st
from Feature_01 import return_even
from Feature_02 import return_odd

st.set_page_config(
    page_title="FridgeBoss", 
    layout="wide")

#Titel + introduction
st.title("Hallo bei FridgeBoss")

st.subheader("Namen angeben")
name = st.text_input("Bitte Namen eingeben", placeholder= "Dein Name ist...")
if name != "":
    st.write(f"Hallo bei FridgeBoss {name}! Ich bin dein persönliches Rezept generiersystem, wie kann ich behilflich sein")

st.subheader("Rezept typ")
if "rezept_typ" not in st.session_state:  # Falls die Variable noch nicht existiert
    st.session_state.rezept_typ = None     # erstelle sie mit dem Wert None

if st.session_state.rezept_typ is None:
    st.write("Bitte wählen sie aus was für ein Rezept sie sich wünschen")

col1, col2, col3 = st.columns(3) # alle buttons auf eine höhe packen


if col1.button ("🌱Vegan" if st.session_state.rezept_typ != "Vegan" else "✅ Vegan", key = "btn_Vegan"): 
    st.session_state.rezept_typ = "Vegan"
elif col2.button ("🥗Vegetarisch" if st.session_state.rezept_typ != "Vegetarisch" else "✅ Vegetarisch", key = "btn_Vegetarisch"):
    st.session_state.rezept_typ = "Vegetarisch"
elif col3.button ("🍖Allesesser" if st.session_state.rezept_typ != "Allesesser" else "✅ Allesesser", key = "btn_allesesser"):
    st.session_state.rezept_typ = "Allesesser"

# Anzeige nach Auswahl
if st.session_state.rezept_typ == "Vegan":
    st.write("Sie wünschen sich also ein Veganes Rezept!")
elif st.session_state.rezept_typ == "Vegetarisch":
    st.write("Sie wünschen sich also ein Vegetarisches Rezept!")
elif st.session_state.rezept_typ == "Allesser":
    st.write("Sie wünschen sich also ein normales Rezept")


original_list = [i for i in range(10)]

even_list = return_even(original_list)

odd_list = return_odd(original_list)

st.write("Hooray, we connected everything")

st.write(even_list)

st.write(odd_list)

