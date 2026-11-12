import streamlit as st
import json
import base64

from pathlib import Path
from st_click_detector import click_detector

from backend.database.chat_repository import (
    create_work_order,
    get_work_orders,
    update_work_order
)


# =====================================
# LOAD EQUIPMENT DETAILS
# =====================================

def load_equipment_details(project_dir):

    equipment_path = (
        project_dir
        / "backend"
        / "data"
        / "equipment_data.json"
    )

    if not equipment_path.exists():
        return []

    with open(equipment_path, "r", encoding="utf-8") as file:
        return json.load(file)


# =====================================
# DISPLAY EQUIPMENT DETAILS
# =====================================

def render_equipment_details(selected_equipment, equipment_details):

    selected_details = next(
        (
            item for item in equipment_details
            if item["equipment_id"] == selected_equipment
        ),
        None
    )

    if selected_details is None:
        st.warning("No details available for this equipment.")
        return

    st.divider()
    st.subheader("Equipment Details")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Equipment ID", selected_details["equipment_id"])

    with col2:
        st.metric("Equipment Type", selected_details["type"])

    st.write("**Equipment Name:**")
    st.write(selected_details["name"])

    st.write("**Description:**")
    st.write(selected_details["description"])


# =====================================
# CREATE WORK ORDER
# =====================================

def render_create_work_order(equipment_id):

    st.subheader("Create Maintenance Work Order")

    with st.form("create_work_order_form", clear_on_submit=True):

        description = st.text_area("Problem Description")

        technician = st.text_input("Technician Name")

        maintenance_type = st.selectbox(
            "Maintenance Type",
            [
                "Preventive",
                "Corrective",
                "Inspection",
                "Breakdown",
                "Predictive"
            ]
        )

        action_taken = st.text_area("Action Taken")

        parts_used = st.text_input("Parts Used")

        cost = st.number_input(
            "Maintenance Cost (₹)",
            min_value=0.0,
            value=0.0,
            step=100.0
        )

        submitted = st.form_submit_button(
            "Create Work Order",
            use_container_width=True
        )

        if submitted:

            if not description.strip():
                st.error("Please enter a problem description.")

            else:

                work_order_id = create_work_order(
                    equipment_id,
                    description.strip(),
                    technician,
                    maintenance_type,
                    action_taken,
                    parts_used,
                    cost
                )

                st.success(
                    f"Work Order #{work_order_id} created successfully!"
                )

                st.rerun()


# =====================================
# VIEW EXISTING WORK ORDERS
# =====================================

def render_existing_work_orders(equipment_id):

    st.divider()
    st.subheader("Existing Maintenance Work Orders")

    work_orders = get_work_orders(equipment_id)

    if not work_orders:
        st.info("No work orders found for this equipment.")
        return

    for order in work_orders:

        with st.expander(
            f"Work Order #{order['work_order_id']} | {order['status']}"
        ):

            st.write("**Description:**", order["description"])
            st.write("**Technician:**", order["technician"])
            st.write("**Maintenance Type:**", order["maintenance_type"])
            st.write("**Action Taken:**", order["action_taken"])
            st.write("**Parts Used:**", order["parts_used"])
            st.write("**Cost:** ₹", order["cost"])
            st.write("**Created:**", order["created_at"])
            st.write("**Last Updated:**", order["updated_at"])


# =====================================
# UPDATE WORK ORDER
# =====================================

def render_update_work_order(equipment_id):

    st.divider()
    st.subheader("Update Maintenance Work Order")

    work_orders = get_work_orders(equipment_id)

    if not work_orders:
        st.info("No work orders available to update.")
        return

    selected_order_id = st.selectbox(
        "Select Work Order",
        options=[order["work_order_id"] for order in work_orders],
        format_func=lambda order_id: f"Work Order #{order_id}"
    )

    selected_order = next(
        order for order in work_orders
        if order["work_order_id"] == selected_order_id
    )

    maintenance_types = [
        "Preventive",
        "Corrective",
        "Inspection",
        "Breakdown",
        "Predictive"
    ]

    statuses = [
        "Open",
        "In Progress",
        "Completed",
        "Closed"
    ]

    with st.form(f"update_work_order_{selected_order_id}"):

        description = st.text_area(
            "Problem Description",
            value=selected_order["description"]
        )

        technician = st.text_input(
            "Technician Name",
            value=selected_order["technician"] or ""
        )

        current_type = selected_order["maintenance_type"]

        maintenance_type = st.selectbox(
            "Maintenance Type",
            maintenance_types,
            index=(
                maintenance_types.index(current_type)
                if current_type in maintenance_types else 0
            )
        )

        action_taken = st.text_area(
            "Action Taken",
            value=selected_order["action_taken"] or ""
        )

        parts_used = st.text_input(
            "Parts Used",
            value=selected_order["parts_used"] or ""
        )

        cost = st.number_input(
            "Maintenance Cost (₹)",
            min_value=0.0,
            value=float(selected_order["cost"] or 0),
            step=100.0
        )

        current_status = selected_order["status"]

        status = st.selectbox(
            "Work Order Status",
            statuses,
            index=(
                statuses.index(current_status)
                if current_status in statuses else 0
            )
        )

        updated = st.form_submit_button(
            "Update Work Order",
            use_container_width=True
        )

        if updated:

            if not description.strip():
                st.error("Description cannot be empty.")

            else:

                update_work_order(
                    work_order_id=selected_order_id,
                    description=description.strip(),
                    technician=technician,
                    maintenance_type=maintenance_type,
                    action_taken=action_taken,
                    parts_used=parts_used,
                    cost=cost,
                    status=status
                )

                st.success(
                    f"Work Order #{selected_order_id} updated successfully!"
                )

                st.rerun()


# =====================================
# MAIN P&ID VIEW
# =====================================

def render_blueprint_view():

    st.subheader("Interactive P&ID Asset Explorer")

    st.write("Click on any equipment to view its details.")

    project_dir = Path(__file__).resolve().parents[2]

    image_path = (
        project_dir
        / "frontend"
        / "assets"
        / "blueprint.png"
    )

    json_path = (
        project_dir
        / "backend"
        / "data"
        / "blueprint_coords.json"
    )

    if not image_path.exists():
        st.error("Blueprint image not found!")
        return

    if not json_path.exists():
        st.error("Equipment coordinates file not found!")
        return

    try:

        with open(json_path, "r", encoding="utf-8") as file:
            equipment_nodes = json.load(file)

    except (json.JSONDecodeError, OSError):

        st.error("Unable to load equipment coordinates.")
        return

    equipment_details = load_equipment_details(project_dir)

    if not equipment_details:
        st.error("Equipment details file is missing or empty.")
        return

    with open(image_path, "rb") as file:
        image_base64 = base64.b64encode(file.read()).decode()

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

    full_html = (
        css
        + '<div class="blueprint-container">'
        + f'<img src="data:image/png;base64,{image_base64}" class="blueprint-img">'
        + "".join(html_elements)
        + "</div>"
    )

    clicked_equipment = click_detector(full_html)

    if clicked_equipment:
        st.session_state["selected_equipment"] = clicked_equipment

    selected_equipment = st.session_state.get("selected_equipment")

    if selected_equipment:

        render_equipment_details(
            selected_equipment,
            equipment_details
        )

        render_create_work_order(selected_equipment)

        render_existing_work_orders(selected_equipment)

        render_update_work_order(selected_equipment)

    else:

        st.info("Select equipment from the P&ID diagram.")