import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data

# 5. Streamlit User Interface
# ----------------------------

def calculate_bmi(weight, height):
    """Calculate BMI given weight (kg) and height (m)."""
    return weight / (height ** 2)

def recommend_based_on_bmi_and_goal(bmi, goal, activity_level, age, df):
    """
    Recommend recipes based on BMI, goal (e.g., weight loss, weight gain, etc.), 
    activity level, and age.
    """
    # Adjust calorie recommendation based on activity level
    if activity_level == 'Sedentary':
        calorie_multiplier = 1.2
    elif activity_level == 'Lightly active':
        calorie_multiplier = 1.375
    elif activity_level == 'Moderately active':
        calorie_multiplier = 1.55
    elif activity_level == 'Very active':
        calorie_multiplier = 1.725
    else:
        calorie_multiplier = 1.9

    # Adjust based on age (calorie needs slightly decrease as you age)
    if age < 30:
        age_multiplier = 1.0
    elif 30 <= age <= 50:
        age_multiplier = 0.95
    else:
        age_multiplier = 0.90

    # Adjust based on the goal
    if goal == "Weight Loss":
        recommended = df[df['calories'] <= df['calories'].quantile(0.25) * calorie_multiplier * age_multiplier]
    elif goal == "Weight Gain":
        recommended = df[df['calories'] >= df['calories'].quantile(0.75) * calorie_multiplier * age_multiplier]
    else:  # Staying Healthy
        recommended = df[df['calories'] <= df['calories'].quantile(0.75) * calorie_multiplier * age_multiplier]
    
    return recommended, goal



# ----------------------------
# Main Streamlit App
# ----------------------------

def main():
    # Adding custom styles to center the form and change background color
    st.markdown("""
        <style>
            .centered {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                background-color: #f5f5f5;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            }
            .block-container {
                padding-top: 3rem;
                padding-bottom: 3rem;
            }
            .stButton>button {
                background-color: #00bfff;
                color: white;
                border: none;
                padding: 0.5em 2em;
                border-radius: 10px;
                font-size: 16px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Centering title
    st.markdown("<h1 style='text-align: center;'>AI Nutritional Meal Planner</h1>", unsafe_allow_html=True)
    
    with st.form("user_input_form"):
        st.markdown("<div class='centered'>", unsafe_allow_html=True)
        
        # User inputs for age, weight, height, activity level, and goal
        age = st.number_input("Enter your age", min_value=10, max_value=100, value=10)
        weight = st.number_input("Enter your weight (kg)", min_value=30.0, max_value=200.0, value=30.0)
        height = st.number_input("Enter your height (m)", min_value=1.0, max_value=2.5, value=1.0)
        
        activity_level = st.selectbox("Select your activity level", 
                                      ["Sedentary", "Lightly active", "Moderately active", "Very active", "Super active"])
        
        goal = st.selectbox("What's your goal?", ["Weight Loss", "Weight Gain", "Staying Healthy"])
        
        submit_button = st.form_submit_button("Get Recommendations")
        
        st.markdown("</div>", unsafe_allow_html=True)

    if submit_button:
        bmi = calculate_bmi(weight, height)
        st.markdown(f"<h2 style='text-align: center;'>Your BMI: {bmi:.2f}</h2>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()