
import streamlit as st
import pandas as pd
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Papaw's Workout Tracker", layout="wide")

# Google Sheets setup
def save_to_gsheet(dataframe):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
        sheet = client.open("Papaw's Workout Log").sheet1

        rows = dataframe.values.tolist()
        for row in rows:
            sheet.append_row(row, value_input_option="USER_ENTERED")

        st.success("Data saved to Google Sheets.")
    except Exception as e:
        st.error(f"Failed to connect or write to Google Sheets: {e}")

st.title("Papaw's Workout Tracker – Day 1: Chest & Triceps")

selected_date = st.date_input("Workout Date", value=date.today())
body_weight = st.number_input("Your Body Weight (lbs)", min_value=80, max_value=400, value=201)

exercises = [
    "Incline Dumbbell Press",
    "Flat Bench Press",
    "Dumbbell or Cable Chest Flyes",
    "Dips (Assisted or Bodyweight)",
    "Overhead Triceps Extension",
    "Rope Triceps Pushdown"
]

all_data = []

for exercise in exercises:
    with st.expander(exercise):
        num_sets = st.number_input(f"How many sets for {exercise}?", min_value=1, max_value=10, value=3, key=f"{exercise}_sets")
        for set_num in range(1, num_sets + 1):
            cols = st.columns(2)
            reps = cols[0].number_input(f"Reps (Set {set_num})", min_value=1, max_value=100, value=10, key=f"{exercise}_reps_{set_num}")
            weight = cols[1].number_input(f"Weight (lbs, Set {set_num})", min_value=1, max_value=1000, value=100, key=f"{exercise}_weight_{set_num}")
            # Simple METs-based calorie formula
            calories = (6 * 3.5 * (body_weight / 2.2) / 200) * (reps * 2 / 60)

            all_data.append({
                "Date": str(selected_date),
                "Day": "Day 1 – Chest & Triceps",
                "Exercise": exercise,
                "Set": set_num,
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
    df = pd.DataFrame(all_data)
    save_to_gsheet(df)
