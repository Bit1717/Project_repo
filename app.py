import streamlit as st
import sqlite3
import os 
import Feature_01 for virtuellen Kühlschrank


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

ingredients = st.multiselect(
    "Welche Zutaten hast du zu Hause?",
    [
        "Tomate", "Milch", "Reis", "Käse", "Ei",
        "Brokkoli", "Tofu", "Zwiebel", "Knoblauch",
        "Pasta", "Chicken", "Salat", "Karotte", "Kartoffel"
    ]
)

st.markdown("## 🧊 Dein digitaler Kühlschrank")

ingredient_icons = {
    "Tomate": "🍅",
    "Milch": "🥛",
    "Reis": "🍚",
    "Käse": "🧀",
    "Ei": "🥚",
    "Brokkoli": "🥦",
    "Tofu": "🧊",
    "Zwiebel": "🧅",
    "Knoblauch": "🧄",
    "Pasta": "🍝",
    "Chicken": "🍗",
    "Salat": "🥬",
    "Karotte": "🥕",
    "Kartoffel": "🥔"
}

expiry_status = {
    "Milch": "soon",
    "Tomate": "soon",
    "Käse": "medium",
    "Ei": "medium",
    "Reis": "ok",
    "Pasta": "ok",
    "Kartoffel": "ok"
}

def get_card_color(status):
    if status == "soon":
        return "#ffe3e3"   # bald ablaufend
    elif status == "medium":
        return "#fff3cd"   # mittel
    else:
        return "#e6f4ea"   # frisch / ok
if ingredients:
    st.markdown(
        """
        <div style="
            border: 3px solid #d0d7de;
            border-radius: 24px;
            padding: 24px;
            background: linear-gradient(180deg, #f8fafc, #e9eef5);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        ">
        """,
        unsafe_allow_html=True
    )

    cols = st.columns(4)

    for i, ingredient in enumerate(ingredients):
        icon = ingredient_icons.get(ingredient, "🥫")
        status = expiry_status.get(ingredient, "ok")
        color = get_card_color(status)

        if status == "soon":
            label = "läuft bald ab"
        elif status == "medium":
            label = "bald verwenden"
        else:
            label = "frisch"
        with cols[i % 4]:
            st.markdown(
                f"""
                <div style="
                    background-color: {color};
                    border-radius: 18px;
                    padding: 18px;
                    text-align: center;
                    margin-bottom: 14px;
                    border: 1px solid #d8dee4;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.06);
                ">
                    <div style="font-size: 44px;">{icon}</div>
                    <div style="font-size: 17px; font-weight: 700; margin-top: 6px;">
                        {ingredient}
                    </div>
                    <div style="font-size: 12px; color: #57606a; margin-top: 4px;">
                        {label}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    st.caption("🔴 läuft bald ab · 🟡 bald verwenden · 🟢 frisch")

else:
    st.info("Wähle Zutaten aus, um deinen digitalen Kühlschrank zu sehen.")



# Digitaler Kühlschrank

ingredient_icons = {
    "Tomate": "🍅",
    "Milch": "🥛",
    "Reis": "🍚",
    "Käse": "🧀",
    "Ei": "🥚",
    "Brokkoli": "🥦",
    "Tofu": "🧊",
    "Zwiebel": "🧅",
    "Knoblauch": "🧄",
    "Pasta": "🍝",
    "Chicken": "🍗",
    "Salat": "🥬",
    "Karotte": "🥕",
    "Kartoffel": "🥔"
}

st.markdown("## 🧊 Dein digitaler Kühlschrank")

if ingredients:
    cols = st.columns(4)

    for i, ingredient in enumerate(ingredients):
        with cols[i % 4]:
            icon = ingredient_icons.get(ingredient, "🥫")

            st.markdown(
                f"""
                <div style="
                    background-color: #f3f6f8;
                    border-radius: 15px;
                    padding: 18px;
                    text-align: center;
                    margin-bottom: 12px;
                    border: 1px solid #dfe4ea;
                ">
                    <div style="font-size: 42px;">{icon}</div>
                    <div style="font-size: 16px; font-weight: bold;">
                        {ingredient}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.info("Wähle Zutaten aus, um deinen digitalen Kühlschrank zu sehen.")

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
        max_value=100,
        value=25,
        step=5
    )

    # Number of servings
    portionen = st.number_input(
        "👥 Anzahl Personen",
        min_value=1,
        max_value=10,
        value=2
    )
    
