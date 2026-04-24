import streamlit as st
import sqlite3
import os 
from Feature_01 import return_even
from Feature_02 import return_odd

def create_gitignore():
    """Creates a .gitignore file automatically if it doesn't exist."""
    if not os.path.exists(".gitignore"):
        with open(".gitignore", "w") as f:
            f.write("""# Database
fridgechef.db
 
# Python cache
__pycache__/
*.pyc
 
# Virtual environment
.venv/
 
# Environment variables / secrets
.env
""")

def init_db():
    #create a database if not already there
    conn = sqlite3.connect("fridgechef.db")
    c = conn.cursor()
    c.execute("""
              CREATE TABLE IF NOT EXISTS users(
                  id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT UNIQUE NOT NULL,
                rezept_typ TEXT
              )
              """)
    conn.commit ()
    conn.close ()

def save_user(name: str, rezept_typ: str):
    """Save or update a user and their meal preference."""
    conn = sqlite3.connect("fridgechef.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (name, rezept_typ)
        VALUES (?, ?)
        ON CONFLICT(name) DO UPDATE SET
            rezept_typ = excluded.rezept_typ
    """, (name, rezept_typ))
    conn.commit()
    conn.close()
 
def load_users() -> list:
    """Load all saved usernames."""
    conn = sqlite3.connect("fridgechef.db")
    c = conn.cursor()
    c.execute("SELECT name FROM users ORDER BY name")
    names = [row[0] for row in c.fetchall()]
    conn.close()
    return names
 
def load_user_preference(name: str) -> str | None:
    """Load the saved meal preference for a specific user."""
    conn = sqlite3.connect("fridgechef.db")
    c = conn.cursor()
    c.execute("SELECT rezept_typ FROM users WHERE name = ?", (name,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

create_gitignore()  # creates .gitignore if missing
init_db()           # creates database if missing



    
st.set_page_config(
    page_title="FridgeBoss", 
    layout="wide")

#Titel + introduction
st.title("Hallo bei FridgeBoss")

st.subheader("Namen angeben")
saved_names = load_users()
with st.columns([3, 1])[0]:
    if saved_names:
        options = ["✏️ Neuen Namen eingeben"] + saved_names
        selected = st.selectbox("Gespeicherte Namen", options)
 
        if selected == "✏️ Neuen Namen eingeben":
            name = st.text_input("Neuen Namen eingeben", placeholder="Dein Name...")
        else:
            name = selected
    else:
        name = st.text_input("Bitte Namen eingeben", placeholder= "Dein Name ist...")
        
if name != "":
    st.write(f"Hallo bei FridgeBoss {name}! Ich bin dein persönliches Rezept generiersystem, wie kann ich behilflich sein")

if name:
    saved_pref = load_user_preference(name)
 
    if saved_pref:
        st.success(f"Willkommen zurück, **{name}**! 👋 Deine letzte Wahl: **{saved_pref}**")
    else:
        st.write(f"Hallo bei FridgeBoss **{name}**! Ich bin dein persönliches Rezeptgenerierungssystem.")
 
    if "rezept_typ" not in st.session_state or st.session_state.get("last_name") != name:
        st.session_state.rezept_typ = saved_pref
        st.session_state.last_name  = name

st.subheader("Rezept typ")
if "rezept_typ" not in st.session_state:  # Falls die Variable noch nicht existiert
    st.session_state.rezept_typ = None     # erstelle sie mit dem Wert None

if st.session_state.rezept_typ is None:
    st.write("Bitte wählen sie aus was für ein Rezept sie sich wünschen")

col1, col2, col3 = st.columns(3) # alle buttons auf eine höhe packen


if col1.button("🌱 Vegan", key="btn_vegan"):
    st.session_state.rezept_typ = "Vegan"
    if name:
        save_user(name, "Vegan")
if col2.button("🥗 Vegetarisch", key="btn_vegetarisch"):
    st.session_state.rezept_typ = "Vegetarisch"
    if name:
        save_user(name, "Vegetarisch")
if col3.button("🍖 Allsesser", key="btn_allesser"):
    st.session_state.rezept_typ = "Allsesser"
    if name:
        save_user(name, "Allesesser")


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

