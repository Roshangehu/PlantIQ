import streamlit as st
import json
import base64

from pathlib import Path
from st_click_detector import click_detector


def render_blueprint_view():

    st.subheader("Interactive P&ID Asset Explorer")

    st.write("Click on any equipment to select it.")

    # Locate project directories
    project_dir = Path(__file__).resolve().parents[2]

    image_path = project_dir / "frontend" / "assets" / "blueprint.png"

    json_path = project_dir / "backend" / "data" / "blueprint_coords.json"

    # Check files
    if not image_path.exists():
        st.error("Blueprint image not found!")
        return

    if not json_path.exists():
        st.error("Equipment coordinates file not found!")
        return

    # Load equipment coordinates
    with open(json_path, "r", encoding="utf-8") as file:
        equipment_nodes = json.load(file)

    # Convert image into Base64
    with open(image_path, "rb") as file:
        image_base64 = base64.b64encode(file.read()).decode()

    # CSS for clickable equipment areas
    css = """
    <style>
        .blueprint-container {
            position: relative;
            width: 100%;
        }

        .blueprint-img {
            width: 100%;
            height: auto;
            display: block;
        }

        .equipment-box {
            position: absolute;
            background-color: transparent;
            border: 2px solid transparent;
            cursor: pointer;
            display: block;
            z-index: 10;
        }

        .equipment-box:hover {
            background-color: rgba(0, 255, 0, 0.25);
            border-color: lime;
        }
    </style>
    """

    # Create clickable areas
    html_elements = []

    for node in equipment_nodes:

        equipment_id = node["equipment_id"]

        left = float(node["x_min"]) * 100
        top = float(node["y_min"]) * 100

        width = (
            float(node["x_max"]) - float(node["x_min"])
        ) * 100

        height = (
            float(node["y_max"]) - float(node["y_min"])
        ) * 100

        overlay = f"""
        <a
            href="#"
            id="{equipment_id}"
            class="equipment-box"
            style="
                left: {left}%;
                top: {top}%;
                width: {width}%;
                height: {height}%;
            ">
        </a>
        """

        html_elements.append(overlay)

    # Combine image and clickable areas
    full_html = (
        css
        + '<div class="blueprint-container">'
        + f'<img src="data:image/png;base64,{image_base64}" class="blueprint-img">'
        + "".join(html_elements)
        + "</div>"
    )

    # Detect clicks
    clicked_equipment = click_detector(full_html)

    if clicked_equipment:
        st.session_state["selected_equipment"] = clicked_equipment

    # Display selected equipment
    selected_equipment = st.session_state.get("selected_equipment")

    if selected_equipment:
        st.success(f"Selected Equipment: {selected_equipment}")
    else:
        st.info("Select an equipment item from the blueprint.")