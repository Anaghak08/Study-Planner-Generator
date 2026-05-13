import streamlit as st
from datetime import date, timedelta
import pandas as pd

st.set_page_config(page_title="Study Planner", layout="centered")

st.title("📚 Study Planner Generator")
st.write("Create a smart daily study plan for your exams")

# Inputs
subjects_input = st.text_area(
    "Enter subjects (comma separated)",
    placeholder="Math, Physics, Chemistry"
)

exam_date = st.date_input("Select exam date")
start_date = date.today()

hours_per_day = st.slider("Study hours per day", 1, 12, 4)

def generate_plan(subjects, start, end, hours):
    days = (end - start).days

    if days <= 0:
        return None

    plan = []
    subject_index = 0

    for i in range(days):
        current_day = start + timedelta(days=i)
        subject = subjects[subject_index]

        plan.append({
            "Date": current_day.strftime("%Y-%m-%d"),
            "Subject": subject,
            "Study Hours": hours
        })

        subject_index = (subject_index + 1) % len(subjects)

    return pd.DataFrame(plan)

if st.button("Generate Plan"):
    if not subjects_input.strip():
        st.error("Please enter subjects")
    else:
        subjects = [s.strip() for s in subjects_input.split(",") if s.strip()]

        plan_df = generate_plan(subjects, start_date, exam_date, hours_per_day)

        if plan_df is None:
            st.error("Exam date must be in the future")
        else:
            st.success("✅ Study plan generated!")

            st.dataframe(plan_df, use_container_width=True)

            # Download
            csv = plan_df.to_csv(index=False)

            st.download_button(
                label="📥 Download Plan (CSV)",
                data=csv,
                file_name="study_plan.csv",
                mime="text/csv"
            )
