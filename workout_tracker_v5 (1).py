
import streamlit as st
import pandas as pd
from datetime import date
import os

EXERCISE_MET_VALUES = {
    "Incline Dumbbell Press": 6.0,
    "Flat Bench Press": 6.0,
    "Dumbbell/Cable Chest Flyes": 5.5,
    "Dips": 5.5,
    "Overhead Triceps Extension": 4.0,
    "Rope Triceps Pushdown": 4.0,
    "Pull-Ups/Lat Pulldown": 6.0,
    "Bent Over Barbell Rows": 6.0,
    "Seated Cable Row": 5.5,
    "Face Pulls": 4.0,
    "Barbell/EZ-Bar Curl": 4.0,
    "Hammer Curls": 4.0,
    "Barbell/Hack Squats": 7.0,
    "Leg Press": 6.5,
    "Romanian Deadlifts": 6.0,
    "Seated Leg Curl": 5.0,
    "Standing/Seated Calf Raises": 4.5,
    "Seated DB Shoulder Press": 5.5,
    "Lateral Raises": 4.0,
    "Rear Delt Flyes": 4.0,
    "Front Raises": 4.0,
    "Plank": 3.0,
    "Hanging Leg Raises/Cable Crunch": 4.0,
    "Push-Ups": 6.0,
    "Pull-Ups": 6.0,
    "Dumbbell Bench Press": 6.0,
    "Dumbbell Rows": 6.0,
    "Arnold Press": 6.0,
    "Barbell Curl + Triceps Rope Superset": 6.5
}

workout_plan = {
    "Day 1 – Chest & Triceps": [
        "Incline Dumbbell Press", "Flat Bench Press", "Dumbbell/Cable Chest Flyes",
        "Dips", "Overhead Triceps Extension", "Rope Triceps Pushdown"
    ],
    "Day 2 – Back & Biceps": [
        "Pull-Ups/Lat Pulldown", "Bent Over Barbell Rows", "Seated Cable Row",
        "Face Pulls", "Barbell/EZ-Bar Curl", "Hammer Curls"
    ],
    "Day 3 – Legs (No Lunges)": [
        "Barbell/Hack Squats", "Leg Press", "Romanian Deadlifts",
        "Seated Leg Curl", "Standing/Seated Calf Raises"
    ],
    "Day 4 – Shoulders & Abs": [
        "Seated DB Shoulder Press", "Lateral Raises", "Rear Delt Flyes",
        "Front Raises", "Plank", "Hanging Leg Raises/Cable Crunch"
    ],
    "Day 5 – Full Upper + HIIT": [
        "Push-Ups", "Pull-Ups", "Dumbbell Bench Press",
        "Dumbbell Rows", "Arnold Press", "Barbell Curl + Triceps Rope Superset"
    ]
}

st.set_page_config(page_title="Papaw's Workout Tracker", layout="wide")
st.title("Papaw’s Workout Tracker")

selected_day = st.selectbox("Select Workout Day", list(workout_plan.keys()))
selected_date = st.date_input("Workout Date", value=date.today())
body_weight = st.number_input("Your Body Weight (lbs)", min_value=80, max_value=400, value=201)

exercise_data = []

st.subheader("Workout Logging")
for exercise in workout_plan[selected_day]:
    with st.expander(f"{exercise}"):
        num_sets = st.number_input(f"{exercise} – Sets", min_value=1, max_value=10, value=4, key=f"{exercise}_sets")
        for set_num in range(1, num_sets + 1):
            col1, col2 = st.columns(2)
            with col1:
                reps = st.number_input(f"Set {set_num} Reps", min_value=0, max_value=100, value=10, key=f"{exercise}_reps_{set_num}")
            with col2:
                weight = st.number_input(f"Set {set_num} Weight (lbs)", min_value=0, max_value=1000, value=0, key=f"{exercise}_weight_{set_num}")
            met = EXERCISE_MET_VALUES.get(exercise, 5.0)
            duration_min = reps * 2 / 60
            calories = (met * 3.5 * (body_weight / 2.2) / 200) * duration_min
            exercise_data.append({
                "Date": selected_date,
                "Day": selected_day,
                "Exercise": exercise,
                "Set": set_num,
                "Reps": reps,
                "Weight (lbs)": weight,
                "Calories Burned": round(calories, 2)
            })

with st.expander("Incline Walking – Cardio"):
    cardio_minutes = st.slider("Duration (minutes)", 0, 60, 30)
    cardio_calories = round(cardio_minutes * 6.8)
    st.write(f"Estimated Cardio Calories Burned: **{cardio_calories} kcal**")

with st.expander("Body Measurements"):
    biceps = st.number_input("Biceps (in)", min_value=0.0, max_value=30.0, step=0.1)
    forearms = st.number_input("Forearms (in)", min_value=0.0, max_value=25.0, step=0.1)
    waist = st.number_input("Waist (in)", min_value=0.0, max_value=60.0, step=0.1)
    thigh = st.number_input("Thigh (in)", min_value=0.0, max_value=40.0, step=0.1)

notes = st.text_area("Notes")

if st.button("Save Workout"):
    df = pd.DataFrame(exercise_data)
    df["Cardio (min)"] = cardio_minutes
    df["Cardio Calories"] = cardio_calories
    df["Biceps"] = biceps
    df["Forearms"] = forearms
    df["Waist"] = waist
    df["Thigh"] = thigh
    df["Notes"] = notes

    filename = "workout_log.csv"
    if os.path.exists(filename):
        existing = pd.read_csv(filename)
        df = pd.concat([existing, df], ignore_index=True)

    df.to_csv(filename, index=False)
    st.success("Workout saved successfully!")

if st.checkbox("Show Workout History"):
    try:
        log_df = pd.read_csv("workout_log.csv")
        st.dataframe(log_df)
    except FileNotFoundError:
        st.info("No workout data found yet.")
