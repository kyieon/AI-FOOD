from dotenv import load_dotenv
import os

import google.generativeai as gemini
import streamlit as st


load_dotenv()

API_KEY = os.environ.get("API_KEY")
gemini.configure(api_key=API_KEY)

hide = """
<style>
div[data-testid="stConnectionStatus"] {
    display: none !important;
</style>
"""

st.markdown(hide, unsafe_allow_html=True)


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
        f"Randomly select 10 {selected_menu_type} foods that people like, along with a brief description, and tell us "
        f"how much you like them as a percentage. Please exclude foods that overlap with foods from other countries."
        f"We need to parse the data, so please send us the menu name, description, and percentage table format and sort by percentage."
    )
    text = response.text

    st.divider()

    if text:
        menus = text.split("\n")

        def parse(menus):
            l = []
            if len(menus) == 12:
                for i, menu in enumerate(menus[-10:]):
                    menu_split = menu.replace("*", "").split("|")
                    if len(menu_split) == 3:
                        menu_name = menu_split[0]
                        description = menu_split[1]
                        percent = menu_split[2]
                    else:
                        menu_name = menu_split[1]
                        description = menu_split[2]
                        percent = menu_split[3]
                    l.append((menu_name, description, percent))
            elif len(menus) == 11:
                for i, menu in enumerate(menus[-9:]):
                    menu_split = menu.replace("*", "").split("|")
                    print("menu_split Len:", len(menu_split))
                    if len(menu_split) == 3:
                        menu_name = menu_split[0]
                        description = menu_split[1]
                        percent = menu_split[2]
                    else:
                        menu_name = menu_split[1]
                        description = menu_split[2]
                        percent = menu_split[3]
                    l.append((menu_name, description, percent))
            else:
                for i, menu in enumerate(menus):
                    menu_split = menu.split("**")
                    print("menu_split Len:", len(menu_split))
                    if len(menu_split) == 1:
                        menu_split0_split = menu_split[0].split(" ")
                        menu_name = menu_split0_split[1]
                        description = menu_split0_split[3:]
                        percent = menu_split0_split[2]
                    elif len(menu_split) == 3:
                        menu_split1 = menu_split[1]
                        print("menu_split1 Len:", len(menu_split1))
                        if len(menu_split1) == 1:
                            menu_split_2_split = menu_split[2].split("-")
                            print("1.menu_split1:", menu_split1)
                            print("1.menu_split_2_split:", menu_split_2_split)
                            menu_name = menu_split1[0]
                            description = menu_split_2_split[1]
                            percent = menu_split_2_split[0]
                        else:
                            menu_split1_split = menu_split1.split(" ")
                            print("2.menu_split:", menu_split)
                            print("2.menu_split1_split:", menu_split1_split)
                            menu_name = menu_split1_split[0]
                            description = menu_split[2]
                            percent = menu_split1_split[1]
                    else:
                        print("3.menu_split:", menu_split)
                        menu_name = menu_split[1]
                        description = menu_split[2]
                        percent = menu_split[3]
                    l.append((menu_name, description, percent))
            return l

        for i, menu in enumerate(parse(menus)):
            name, description, percentage = menu

            link = f"https://www.google.com/search?q={name}"

            st.page_link(
                link,
                label=f"{i+1}\\. [{percentage}] {name} ({description})",
                icon=":material/travel_explore:",
            )
