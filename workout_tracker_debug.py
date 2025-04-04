
import streamlit as st
import pandas as pd
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
st.write(Secrets loaded:" list(st.secrets.keys()))
         

def connect_to_gsheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
        sheet = client.open("Papaw’s Workout Log").sheet1
        st.success("Connected to Google Sheets.")
        return sheet
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {e}")
        return None

def save_to_gsheet(dataframe):
    sheet = connect_to_gsheet()
    if sheet:
        try:
            rows = dataframe.values.tolist()
            sheet.append_rows(rows)
            st.success("Data saved to Google Sheets.")
        except Exception as e:
            st.error(f"Failed to save to Google Sheets: {e}")

st.set_page_config(page_title="Papaw's Workout Tracker", layout="wide")
st.title("Papaw’s Workout Tracker – Debug Version")

selected_day = st.selectbox("Select Workout Day", [
    "Day 1 – Chest & Triceps", "Day 2 – Back & Biceps", "Day 3 – Legs (No Lunges)",
    "Day 4 – Shoulders & Abs", "Day 5 – Full Upper + HIIT"
])
selected_date = st.date_input("Workout Date", value=date.today())
body_weight = st.number_input("Your Body Weight (lbs)", min_value=80, max_value=400, value=201)

exercise_data = []
exercise = "Test Exercise"
with st.expander(f"{exercise}"):
    reps = st.number_input("Reps", value=10)
    weight = st.number_input("Weight (lbs)", value=100)
    calories = (6 * 3.5 * (body_weight / 2.2) / 200) * (reps * 2 / 60)
    exercise_data.append({
        "Date": selected_date,
        "Day": selected_day,
        "Exercise": exercise,
        "Set": 1,
        "Reps": reps,
        "Weight (lbs)": weight,
        "Calories Burned": round(calories, 2),
        "Cardio (min)": 0,
        "Cardio Calories": 0,
        "Biceps": 0,
        "Forearms": 0,
        "Waist": 0,
        "Thigh": 0,
        "Notes": ""
    })

if st.button("Save to Google Sheets"):
    df = pd.DataFrame(exercise_data)
    save_to_gsheet(df)
