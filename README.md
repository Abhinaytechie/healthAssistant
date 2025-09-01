# 🏥 Health Assistant App

This project is a **Dialogflow + Flask + OR-Tools + LLM** powered Health Assistant.

A **Streamlit-based Health Assistant** that allows users to:

- **Book doctor appointments in real-time**  
- **Get personalized diet advice** using **DeepSeek LLM**  

This app integrates **real-time scheduling**, **diet advice logic**, and a **user-friendly interactive interface**.

---
## Setup
1. Run `pip install flask ortools`
2. Start backend: `python backend/app.py`
3. Import `dialogflow_agent/` into Dialogflow
---

## Features

### 1. Real-Time Appointment Booking
- Users select doctor specialization (Cardiologist, Dermatologist, etc.)  
- System automatically assigns the **first available slot**  
- Tracks booked slots to avoid **double bookings**  
- Supports **multiple patients and specializations**  

### 2. Diet Advice
- Rule-based advice for common conditions:
  - Diabetes  
  - Weight Loss  
  - Heart Health  
- **DeepSeek LLM Integration**:
  - Provides personalized diet suggestions for less common conditions  
  - Ensures fallback advice if API is unavailable  

### 3. Streamlit Interface
- Single-page interactive UI  
- Sidebar to select between **appointment booking** or **diet advice**  
- Immediate visual feedback to the user  

---

## 💬 Dialogue Flow

The app mimics a conversational flow:

1. **User selects service:**
   - "Book Appointment" → appointment booking form  
   - "Diet Advice" → diet advice form  

2. **Appointment Booking Flow:**
    - User: I want to book an appointment with a Cardiologist
    - App: ✅ Appointment booked with Dr. Ramesh Gupta at 10AM for John Doe


3. **Diet Advice Flow:**
   -  User: I want diet advice for Diabetes
   -  App: 🍎 Focus on high-fiber foods, whole grains, vegetables. Avoid sugary drinks.
