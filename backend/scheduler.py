# ----------------- Real-Time Appointment Scheduler -----------------
booked_slots = {}  # keeps track of booked slots: {doctor_name: [slot1, slot2,...]}

def schedule_real_time(patient, doctors_data, condition="General Physician"):
    """
    Schedules a single appointment in real-time.
    Returns the appointment dict or a message if no slots are available.
    """
    # Filter doctors by specialization
    available_doctors = [
        doc for doc in doctors_data if doc.get("specialization", "").lower() == condition.lower()
    ]
    if not available_doctors:
        return {"message": f"No doctors available for {condition}"}

    # Try to assign first free slot
    for doctor in available_doctors:
        for slot in doctor["available_slots"]:
            if slot not in booked_slots.get(doctor["name"], []):
                # Assign slot
                booked_slots.setdefault(doctor["name"], []).append(slot)
                return {
                    "patient": patient,
                    "doctor": doctor["name"],
                    "slot": slot
                }

    return {"message": f"No available slots for {condition} right now."}
