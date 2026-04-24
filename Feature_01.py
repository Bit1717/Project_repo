import streamlit as st


INGREDIENT_IMAGES = {
    "Tomate": "https://img.spoonacular.com/ingredients_100x100/tomato.png",
    "Milch": "https://img.spoonacular.com/ingredients_100x100/milk.png",
    "Reis": "https://img.spoonacular.com/ingredients_100x100/white-rice.png",
    "Käse": "https://img.spoonacular.com/ingredients_100x100/cheddar-cheese.png",
    "Ei": "https://img.spoonacular.com/ingredients_100x100/egg.png",
    "Brokkoli": "https://img.spoonacular.com/ingredients_100x100/broccoli.png",
    "Tofu": "https://img.spoonacular.com/ingredients_100x100/tofu.png",
    "Zwiebel": "https://img.spoonacular.com/ingredients_100x100/brown-onion.png",
    "Knoblauch": "https://img.spoonacular.com/ingredients_100x100/garlic.png",
    "Pasta": "https://img.spoonacular.com/ingredients_100x100/fusilli.jpg",
    "Chicken": "https://img.spoonacular.com/ingredients_100x100/chicken-breasts.png",
    "Salat": "https://img.spoonacular.com/ingredients_100x100/lettuce.png",
    "Karotte": "https://img.spoonacular.com/ingredients_100x100/carrots.png",
    "Kartoffel": "https://img.spoonacular.com/ingredients_100x100/potatoes-yukon-gold.png",
}


FRIDGE_LAYOUT = {
    "🥛 Oberes Fach": ["Milch", "Käse", "Ei"],
    "🥦 Gemüsefach": ["Tomate", "Brokkoli", "Karotte", "Salat"],
    "🍚 Unteres Fach": ["Reis", "Pasta", "Zwiebel", "Kartoffel"],
    "🥫 Sonstiges": ["Tofu", "Knoblauch", "Chicken"],
}


def show_fridge(ingredients):
    st.markdown("## 🧊 Dein virtueller Kühlschrank")

    if not ingredients:
        st.info("Wähle zuerst Zutaten aus, dann erscheinen sie im virtuellen Kühlschrank.")
        return

    st.markdown(
        """
        <div style="
            border: 5px solid #cbd5e1;
            border-radius: 28px;
            padding: 24px;
            background: linear-gradient(180deg, #f8fafc, #e2e8f0);
            box-shadow: 0 10px 25px rgba(0,0,0,0.10);
        ">
        """,
        unsafe_allow_html=True
    )

    for shelf_name, shelf_items in FRIDGE_LAYOUT.items():
        selected_items = [item for item in shelf_items if item in ingredients]

        st.markdown(f"### {shelf_name}")

        if selected_items:
            cols = st.columns(4)

            for i, item in enumerate(selected_items):
                image_url = INGREDIENT_IMAGES.get(item)

                with cols[i % 4]:
                    st.markdown(
                        """
                        <div style="
                            background-color: white;
                            border-radius: 16px;
                            padding: 16px;
                            text-align: center;
                            margin-bottom: 12px;
                            border: 1px solid #d8dee4;
                            box-shadow: 0 4px 10px rgba(0,0,0,0.06);
                        ">
                        """,
                        unsafe_allow_html=True
                    )

                    if image_url:
                        st.image(image_url, width=90)
                    else:
                        st.write("🥫")

                    st.markdown(f"**{item}**")
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.caption("leer")

        st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)