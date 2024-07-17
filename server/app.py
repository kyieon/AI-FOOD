from dotenv import load_dotenv
import os

import google.generativeai as gemini
import streamlit as st


load_dotenv()

API_KEY = os.environ.get("API_KEY")
gemini.configure(api_key=API_KEY)


@st.cache_resource
def load_model():
    return gemini.GenerativeModel("gemini-pro")


model = load_model()

st.title("Recommend Food")

selected_menu_type = st.selectbox(
    "Please select a food type.",
    [
        "",
        "Korean",
        "Western",
        "Chinese",
        "Japanese",
        "French",
        "Italian",
        "Spanish",
        "German",
        "Mexican",
        "Indian",
        "Thailand",
        "Vietnam",
        "Dessert",
    ],
)

if selected_menu_type != "":
    st.caption(f"You chose is :blue[_{selected_menu_type} Food_]")

    response = model.generate_content(
        f"Please tell me 10 random {selected_menu_type} foods that people like. Leave out the pizza."
    )
    text = response.text

    st.divider()

    if text:
        menus = text.split("\n")

        for i, menu in enumerate(menus):
            mm = menu.split(" ", maxsplit=1)
            menu_name = mm[1]
            link = f"https://www.google.com/search?q={menu_name}"

            st.page_link(
                f"https://www.google.com/search?q={menu_name}",
                label=f"{i+1}\. {menu_name}",
            )
