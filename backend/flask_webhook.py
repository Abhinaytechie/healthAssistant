
from flask import Flask, request, jsonify
from ortools.sat.python import cp_model
import json, os
from diet_advisor import get_diet_advice  # Make sure this is optimized and imported globally

app = Flask(__name__)

# ---------------- Load Data Once ----------------
BASE_DIR = os.path.dirname(__file__)
def load_json_file(path, key):
    try:
        with open(path) as f:
            data = json.load(f)
            return data.get(key, [])
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return []

doctors = load_json_file(os.path.join(BASE_DIR, "data", "doctors.json"), "doctors")


booked_slots = {}  # slot -> patient_name


def schedule_single_patient(patient_name, condition):
    try:
        # Filter doctors
        available_doctors = [d for d in doctors if d['specialization'].lower() == condition.lower()]
        if not available_doctors:
            return {"message": f"No doctors available for {condition}"}

        doctor = available_doctors[0]
        free_slots = [s for s in doctor['available_slots'] if s not in booked_slots]
        print(free_slots)
        if not free_slots:
            return {"message": f"No available slots for {condition} right now."}
    
        # OR-Tools model
        model = cp_model.CpModel()
        x = {s: model.NewBoolVar(f"x_{s}") for s in free_slots}
        model.Add(sum(x.values()) <= 1)
        model.Maximize(sum(x.values()))

        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            for s in free_slots:
                if solver.Value(x[s]) == 1:
                    booked_slots[s] = patient_name
                    return {"patient": patient_name, "doctor": doctor['name'], "slot": s}
        return {"message": f"No available slots for {condition}"}

    except Exception as e:
        print("OR-Tools error:", e)
        return {"message": "⚠️ Scheduling error occurred."}

# ---------------- Flask Webhook ----------------
@app.route("/", methods=["GET"])
def home():
    return "Health Chatbot Webhook Running"
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        req = request.get_json(force=True)
        intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "")

        # ---------- Book Appointment Intent ----------
        if intent == "Book Appointment":
            params = req.get("queryResult", {}).get("parameters", {})
            condition = params.get("condition", "").lower()
            patient_name = params.get("patient_name", "You")
            appointment = schedule_single_patient(patient_name, condition)
            if "message" in appointment:
                fulfillment_text = appointment["message"]
            else:
                fulfillment_text = f"✅ Appointment booked with {appointment['doctor']} at {appointment['slot']} for {appointment['patient']}."
            return jsonify({"fulfillmentText": fulfillment_text})

        # ---------- Diet Advice Intent ----------
        elif intent == "Diet Advice":
            condition = req.get("queryResult", {}).get("parameters", {}).get("condition", "")
            if not condition:
                fulfillment_text = "🥦 Please provide a condition or goal for diet advice."
            else:
                advice = get_diet_advice(condition)
                fulfillment_text = advice
            return jsonify({"fulfillmentText": fulfillment_text})

        # ---------- Fallback ----------
        else:
            return jsonify({"fulfillmentText": "🤔 Sorry, I didn't understand that."})

    except Exception as e:
        print("Webhook error:", e)
        return jsonify({"fulfillmentText": "⚠️ Server error. Please try again later."})

# ---------------- Run Flask ----------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
