import streamlit as st
import sqlite3
import os 


def create_gitignore():
    """Creates a .gitignore file automatically if it doesn't exist."""
    if not os.path.exists(".gitignore"): # checks if .gitignore file does not already exist
        with open(".gitignore", "w") as f: #creates new file called .gitignore
            f.write(""" 
# Database
fridgechef.db
 
# Python cache
__pycache__/
*.pyc
 
# Virtual environment
.venv/
 
# Environment variables / secrets
.env
""") #writes content into the file

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


st.subheader("⚙️ Deine Präferenzen")

# Initialize session state FIRST - before anything uses them
if "rezept_typ"   not in st.session_state: st.session_state.rezept_typ   = None
if "max_kochzeit" not in st.session_state: st.session_state.max_kochzeit = 30
if "kal_min"      not in st.session_state: st.session_state.kal_min      = 300
if "kal_max"      not in st.session_state: st.session_state.kal_max      = 700
if "max_budget"   not in st.session_state: st.session_state.max_budget   = 25.0
if "portionen"    not in st.session_state: st.session_state.portionen    = 2


# Define variables BEFORE the columns
max_kochzeit = st.session_state.max_kochzeit
kal_range    = (st.session_state.kal_min, st.session_state.kal_max)
max_budget   = int(st.session_state.max_budget)
portionen    = st.session_state.portionen


col1, col2 = st.columns(2)

with col1:
    # Cooking time slider
    kochzeit = st.slider(
        "⏱️ Max. Kochzeit (Minuten)",
        min_value=5,
        max_value=120,
        value=30,        # default value
        step=5
    )

    # Calorie slider
    kalorien = st.slider(
        "🔥 Kalorien pro Portion",
        min_value=100,
        max_value=1500,
        value=(300, 700),  # range slider! min and max
        step=50
    )

with col2:
    # Budget slider
    budget = st.slider(
        "💰 Max. Budget (CHF)",
        min_value=5,
        max_value=1000,
        value=25,
        step=5
    )

    # Number of servings
    portionen = st.number_input(
        "👥 Anzahl Personen",
        min_value=1,
        max_value=10,
        value=2,
        step=1        
    )
    # Save button - saves all slider values for this user
if name:
    if st.button("💾 Präferenzen speichern"):
        # Update session state with new values
        st.session_state.max_kochzeit = max_kochzeit
        st.session_state.kal_min      = kal_range[0]
        st.session_state.kal_max      = kal_range[1]
        st.session_state.max_budget   = float(max_budget)
        st.session_state.portionen    = int(float(portionen))
 
        # Save to database
        save_user(
            name,
            max_kochzeit = max_kochzeit,
            kal_min      = kal_range[0],
            kal_max      = kal_range[1],
            max_budget   = float(max_budget),
            portionen    = int(portionen),
        )
        st.success(f"✅ Präferenzen für **{name}** gespeichert!")
else:
    st.info("👆 Bitte zuerst einen Namen eingeben um Präferenzen zu speichern.")

