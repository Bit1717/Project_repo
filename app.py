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

st.subheader("Buttons")
if st.button("About"):
    st.write("This is a Streamlit tutorial for FCS bachelor students!")
    st.write("""
             Streamlit is an open-source Python library designed to simplify the process of creating web applications 
             and interactive dashboards for data science and machine learning. With its intuitive framework, 
             developers and data professionals can transform scripts into shareable web applications in just a few lines
             of code, without requiring any knowledge of web development. 
             At its core, Streamlit operates by rerunning the entire script from top to bottom each time 
             there's an interaction, ensuring that the app's state is always in sync with the user's inputs. 
             To use Streamlit, one simply needs to write a Python script, insert Streamlit-specific functions for 
             interactivity, and then run the script using the streamlit run command. 
             The result is a reactive application hosted locally in a web browser, which can then be easily 
             shared with others. Its seamless integration with data-centric libraries such as Pandas and Matplotlib, 
             along with its growing community and rich ecosystem, makes Streamlit a go-to choice for rapid application
             development in the data domain.
             """)
else:
    st.write("Click the button to learn more about this tutorial.")


original_list = [i for i in range(10)]

even_list = return_even(original_list)

odd_list = return_odd(original_list)

st.write("Hooray, we connected everything")

st.write(even_list)

st.write(odd_list)

