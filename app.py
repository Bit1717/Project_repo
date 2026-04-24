import streamlit as st
import sqlite3
import os 


def create_gitignore():
    """Creates a .gitignore file automatically if it doesn't exist."""
    if not os.path.exists(".gitignore"):
        with open(".gitignore", "w") as f:
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
""")

def init_db():
    """Create users table with ALL preference columns."""
    conn = sqlite3.connect("fridgechef.db")
    c = conn.cursor()
    # FIX 1: added max_kochzeit, kal_min, kal_max, max_budget, portionen columns
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT UNIQUE NOT NULL,
            rezept_typ    TEXT,
            max_kochzeit  INTEGER DEFAULT 30,
            kal_min       INTEGER DEFAULT 300,
            kal_max       INTEGER DEFAULT 700,
            max_budget    REAL    DEFAULT 25,
            portionen     INTEGER DEFAULT 2
        )
    """)
    conn.commit()
    conn.close()

# FIX 2: save_user now accepts all preference parameters
def save_user(name: str, rezept_typ: str = None,
              max_kochzeit: int = None, kal_min: int = None,
              kal_max: int = None, max_budget: float = None,
              portionen: int = None):
    """Save or update a user and their preferences."""
    conn = sqlite3.connect("fridgechef.db")
    c = conn.cursor()

    # Make sure user exists first
    c.execute("INSERT OR IGNORE INTO users (name) VALUES (?)", (name,))

    # Only update fields that were actually provided
    if rezept_typ   is not None:
        c.execute("UPDATE users SET rezept_typ   = ? WHERE name = ?", (rezept_typ,   name))
    if max_kochzeit is not None:
        c.execute("UPDATE users SET max_kochzeit = ? WHERE name = ?", (max_kochzeit, name))
    if kal_min      is not None:
        c.execute("UPDATE users SET kal_min      = ? WHERE name = ?", (kal_min,      name))
    if kal_max      is not None:
        c.execute("UPDATE users SET kal_max      = ? WHERE name = ?", (kal_max,      name))
    if max_budget   is not None:
        c.execute("UPDATE users SET max_budget   = ? WHERE name = ?", (max_budget,   name))
    if portionen    is not None:
        c.execute("UPDATE users SET portionen    = ? WHERE name = ?", (portionen,    name))

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

def load_user_prefs(name: str) -> dict:
    """Load ALL saved preferences for a specific user."""
    conn = sqlite3.connect("fridgechef.db")
    c = conn.cursor()
    c.execute("""
        SELECT rezept_typ, max_kochzeit, kal_min, kal_max, max_budget, portionen
        FROM users WHERE name = ?
    """, (name,))
    row = c.fetchone()
    conn.close()

    if row:
        return {
            "rezept_typ":   row[0],
            "max_kochzeit": row[1] or 30,
            "kal_min":      row[2] or 300,
            "kal_max":      row[3] or 700,
            "max_budget":   row[4] or 25.0,
            "portionen":    row[5] or 2,
        }
    else:
        # Default values for new users
        return {
            "rezept_typ":   None,
            "max_kochzeit": 30,
            "kal_min":      300,
            "kal_max":      700,
            "max_budget":   25.0,
            "portionen":    2,
        }

# =============================================================================
# SETUP
# =============================================================================

create_gitignore()
init_db()

# =============================================================================
# APP
# =============================================================================

st.set_page_config(page_title="FridgeBoss", layout="wide")
st.title("Hallo bei FridgeBoss")

# Initialize session state defaults FIRST
if "rezept_typ"   not in st.session_state: st.session_state.rezept_typ   = None
if "max_kochzeit" not in st.session_state: st.session_state.max_kochzeit = 30
if "kal_min"      not in st.session_state: st.session_state.kal_min      = 300
if "kal_max"      not in st.session_state: st.session_state.kal_max      = 700
if "max_budget"   not in st.session_state: st.session_state.max_budget   = 25.0
if "portionen"    not in st.session_state: st.session_state.portionen    = 2

# =============================================================================
# NAME INPUT
# =============================================================================

st.subheader("👤 Namen angeben")
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
        name = st.text_input("Bitte Namen eingeben", placeholder="Dein Name ist...")

if name:
    # When user changes → reload ALL preferences from database
    if st.session_state.get("last_name") != name:
        prefs = load_user_prefs(name)
        st.session_state.rezept_typ   = prefs["rezept_typ"]
        st.session_state.max_kochzeit = prefs["max_kochzeit"]
        st.session_state.kal_min      = prefs["kal_min"]
        st.session_state.kal_max      = prefs["kal_max"]
        st.session_state.max_budget   = prefs["max_budget"]
        st.session_state.portionen    = prefs["portionen"]
        st.session_state.last_name    = name

    if st.session_state.rezept_typ:
        st.success(f"Willkommen zurück, **{name}**! 👋 Deine letzte Wahl: **{st.session_state.rezept_typ}**")
    else:
        st.write(f"Hallo bei FridgeBoss **{name}**! Ich bin dein persönliches Rezeptgenerierungssystem.")

st.divider()

# =============================================================================
# MEAL TYPE BUTTONS
# =============================================================================

st.subheader("🍽️ Rezept Typ")

if st.session_state.rezept_typ is None:
    st.write("Bitte wählen sie aus was für ein Rezept sie sich wünschen")

col1, col2, col3 = st.columns(3)

if col1.button("🌱 Vegan", key="btn_vegan"):
    st.session_state.rezept_typ = "Vegan"
    if name:
        save_user(name, rezept_typ="Vegan")

if col2.button("🥗 Vegetarisch", key="btn_vegetarisch"):
    st.session_state.rezept_typ = "Vegetarisch"
    if name:
        save_user(name, rezept_typ="Vegetarisch")

if col3.button("🍖 Allesser", key="btn_allesser"):
    st.session_state.rezept_typ = "Allesser"
    if name:
        save_user(name, rezept_typ="Allesser")

if st.session_state.rezept_typ == "Vegan":
    st.success("✅ Sie wünschen sich also ein Veganes Rezept!")
elif st.session_state.rezept_typ == "Vegetarisch":
    st.success("✅ Sie wünschen sich also ein Vegetarisches Rezept!")
elif st.session_state.rezept_typ == "Allesser":
    st.success("✅ Sie wünschen sich also ein normales Rezept!")

st.divider()

# =============================================================================
# SLIDERS - FIX 3: use session state values so sliders load per user
# =============================================================================

st.subheader("⚙️ Deine Präferenzen")

col_left, col_right = st.columns(2)

with col_left:
    max_kochzeit = st.slider(
        "⏱️ Max. Kochzeit (Minuten)",
        min_value=5,
        max_value=120,
        value=int(st.session_state.max_kochzeit),  # loads this user's saved value
        step=5,
    )
    kal_range = st.slider(
        "🔥 Kalorien pro Portion",
        min_value=100,
        max_value=1500,
        value=(int(st.session_state.kal_min), int(st.session_state.kal_max)),  # loads saved range
        step=50,
    )

with col_right:
    max_budget = st.slider(
        "💰 Max. Budget (CHF)",
        min_value=5,
        max_value=1000,
        value=int(st.session_state.max_budget),  # loads this user's saved value
        step=5,
    )
    portionen = st.number_input(
        "👥 Anzahl Personen",
        min_value=1,
        max_value=10,
        value=int(st.session_state.portionen),  # loads this user's saved value
        step=1,
    )

# Save button
if name:
    if st.button("💾 Präferenzen speichern"):
        st.session_state.max_kochzeit = int(max_kochzeit)
        st.session_state.kal_min      = int(kal_range[0])
        st.session_state.kal_max      = int(kal_range[1])
        st.session_state.max_budget   = float(max_budget)
        st.session_state.portionen    = int(float(portionen)) if portionen else 2

        save_user(
            name,
            max_kochzeit = int(max_kochzeit),
            kal_min      = int(kal_range[0]),
            kal_max      = int(kal_range[1]),
            max_budget   = float(max_budget),
            portionen    = int(float(portionen)) if portionen else 2,
        )
        st.success(f"✅ Präferenzen für **{name}** gespeichert!")
else:
    st.info("👆 Bitte zuerst einen Namen eingeben um Präferenzen zu speichern.")