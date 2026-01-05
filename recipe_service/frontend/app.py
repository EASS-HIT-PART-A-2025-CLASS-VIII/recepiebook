import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def parse_ingredients(text: str) -> dict[str, float]:
    """
    Each line: ingredient=amount
    Example:
      flour=200
      milk=300
      egg=2
    """
    result: dict[str, float] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "=" not in line:
            raise ValueError(f"Bad line (missing '='): {line}")
        k, v = line.split("=", 1)
        result[k.strip()] = float(v.strip())
    return result


def parse_steps(text: str) -> list[str]:
    """
    Each line is a step.
    """
    steps = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not steps:
        raise ValueError("Please enter at least 1 step (one per line).")
    return steps


st.set_page_config(page_title="Recipe App", layout="centered")
st.title("🍲 Recipe App")

st.header("Create a new recipe")

with st.form("create_recipe"):
    title = st.text_input("Title")
    description = st.text_input("Description")

    prep_minutes = st.number_input("Prep minutes", min_value=1, value=10, step=1)

    ingredients_text = st.text_area(
        "Ingredients (one per line: name=amount)",
        placeholder="flour=200\nmilk=300\negg=2\nsugar=20",
        height=120,
    )

    steps_text = st.text_area(
        "Steps (one per line)",
        placeholder="Mix ingredients\nPreheat oven to 180C\nBake for 30 minutes",
        height=140,
    )

    submitted = st.form_submit_button("Create recipe")

if submitted:
    try:
        payload = {
            "title": title,
            "description": description,
            "ingredients": parse_ingredients(ingredients_text),
            "steps": parse_steps(steps_text),
            "prep_minutes": int(prep_minutes),
        }

        r = requests.post(f"{API_URL}/recipes", json=payload, timeout=5)
        r.raise_for_status()
        st.success("Recipe created successfully!")
        st.json(r.json())

    except ValueError as ve:
        st.error(str(ve))
    except requests.RequestException:
        st.error("Failed to create recipe")
        try:
            st.json(r.json())  # shows FastAPI validation details if any
        except Exception:
            pass

st.divider()

st.header("All recipes")

try:
    r = requests.get(f"{API_URL}/recipes", timeout=5)
    r.raise_for_status()
    recipes = r.json()

    if not recipes:
        st.info("No recipes yet.")
    else:
        for recipe in recipes:
            with st.expander(f"{recipe['id']}: {recipe['title']}"):
                st.write("**Description:**", recipe.get("description", ""))
                st.write("**Prep minutes:**", recipe.get("prep_minutes", ""))
                st.write("**Ingredients:**")
                st.json(recipe.get("ingredients", {}))
                st.write("**Steps:**")
                st.write("\n".join(f"- {s}" for s in recipe.get("steps", [])))
                
                if st.button(
                    f"🗑️ Delete recipe {recipe['id']}",
                    key=f"delete-{recipe['id']}",
                ):
                    try:
                        del_r = requests.delete(
                            f"{API_URL}/recipes/{recipe['id']}", timeout=5
                        )
                        del_r.raise_for_status()
                        st.success("Recipe deleted")
                        st.rerun()
                    except requests.RequestException:
                        st.error("Failed to delete recipe")

except requests.RequestException as e:
    st.error(f"Failed to load recipes: {e}")
