

import streamlit as st
import requests
import json, os


BASE_DIR = os.path.dirname(__file__)
def load_json_file(path, key):
    try:
        with open(path) as f:
            data = json.load(f)
            return [d["specialization"] for d in data.get(key, [])]
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return []

specializations = load_json_file(os.path.join(BASE_DIR, "data", "doctors.json"), "doctors")


st.set_page_config(page_title="Health Assistant", page_icon="🏥")
st.title("🏥 Health Assistant")

menu = ["Book Appointment", "Diet Advice"]
choice = st.sidebar.selectbox("Select Service", menu)


WEBHOOK_URL = "http://127.0.0.1:5000/webhook"

def call_webhook(intent_name, params):
    payload = {
        "queryResult": {
            "intent": {"displayName": intent_name},
            "parameters": params
        }
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        fulfillment_text = response.json().get("fulfillmentText", "No response from server.")
        return fulfillment_text
    except Exception as e:
        return f"⚠️ Error contacting webhook: {e}"


if choice == "Book Appointment":
    st.header("Book a Doctor Appointment")
    patient_name = st.text_input("Your Name")
    condition = st.selectbox("Choose Doctor Specialization", specializations)

    if st.button("Book Appointment"):
        if not patient_name or not condition:
            st.warning("Please enter your name and select a specialization!")
        else:
            fulfillment_text = call_webhook(
                "Book Appointment",
                {"condition": condition, "patient_name": patient_name}
            )
            if "✅" in fulfillment_text:
                st.success(fulfillment_text)
            else:
                st.error(fulfillment_text)


elif choice == "Diet Advice":
    st.header("Get Personalized Diet Advice")
    condition_input = st.text_input("Enter your condition or goal (e.g., Diabetes, Weight Loss)")

    if st.button("Get Diet Advice"):
        if not condition_input:
            st.warning("Please enter a condition or goal!")
        else:
            fulfillment_text = call_webhook(
                "Diet Advice",
                {"condition": condition_input}
            )
            st.info(fulfillment_text)
