import streamlit as st
import os
import pandas as pd
from utils.data_loader import load_food_data, load_recipe_data
from components.display import display_food, display_recipe
from utils.api_data import get_nutritional_info
from utils.recommendation import calculate_daily_targets
from utils.openai_helper import generate_summary, generate_alternative_food_recommendations

# Page configuration
st.set_page_config(page_title="Tasty Tracker Recommendations",
                   page_icon="🍳",
                   layout="wide")

# Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def show_welcome_page():
    """Display the welcome page"""
    st.markdown("<h1 class='centered-title'>Welcome to Tasty Tracker!</h1>",
                unsafe_allow_html=True)
    st.markdown(
        "<p class='centered-text'>Discover delicious foods and recipes tailored to your preferences and dietary restrictions!</p>",
        unsafe_allow_html=True)
    st.markdown(
        "<p class='centered-text'>But before that, there are 3 simple components we need from you...</p>",
        unsafe_allow_html=True)
    st.markdown(
        "<p class='centered-text'>1) Your recent Food History to find a food that would be complemetary to your personal taste </p>",
        unsafe_allow_html=True)
    st.markdown(
        "<p class='centered-text'>2) Your Physical Metrics so that we better talior recommendations to you bodily needs </p>",
        unsafe_allow_html=True)
    st.markdown(
        "<p class='centered-text'>3) Your Food prefences and Dietary restrictions to follow when finding food to recommend you </p>",
        unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("Next →", type="primary"):
            st.session_state.page = "food_history"
            st.rerun()

def show_food_history_page():
    """Display the food history input page"""
    st.markdown(
        "<div style='text-align: center; margin: 2rem 0 0 0;'><h1>🕐</h1></div>",
        unsafe_allow_html=True)
    # Food history input
    st.subheader("Your Food History")
    food_history = st.text_area(
        "Enter what you've eaten today:",
        value="Today I've eaten: banana, toast with butter, and a glass of whole milk",
        height=100)

    # Next button
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("Next →", type="primary", key="food_history_next"):
            st.session_state.food_history = food_history
            st.session_state.page = "metrics"
            st.rerun()

def show_preferences_page():
    """Display food preferences and restrictions page"""
    st.markdown(
        "<div style='text-align: center; margin: 2rem 0 0 0;'><h1>🍽️</h1></div>",
        unsafe_allow_html=True)
    st.subheader("Food Preferences")

    col1, col2 = st.columns(2)
    with col1:
        cuisine_type = st.selectbox("Cuisine Type", [
            "All", "American", "Italian", "Japanese", "Mexican", "Thai",
            "Chinese", "French"
        ])
        meal_type = st.selectbox(
            "Meal Type", ["All", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert"])

    with col2:
        diet_info = {
            "None": "No specific diet plan selected.",
            "Keto Diet":
            "A high-fat, low-carb diet that aims to put your body in a state of ketosis.",
            "Portfolio Diet":
            "A plant-based diet designed to lower cholesterol and prevent heart disease.",
            "DASH Diet": "Dietary Approaches to Stop Hypertension.",
            "Mediterranean Diet":
            "Emphasizes plant-based foods, whole grains, lean proteins, and healthy fats like olive oil."
        }
        diet_type = st.selectbox("Select Diet Plan", list(diet_info.keys()))
        st.info(diet_info[diet_type])

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Dietary Preferences")
        preferences = st.multiselect("Select Preferences", [
            "Vegetarian", "Vegan", "Low-Calorie", "Low-Fat", "Low-Carb",
            "High-Protein", "Gluten-Free"
        ])

    with col4:
        st.subheader("Allergen Restrictions")
        allergens = st.multiselect(
            "Select Allergens to Avoid",
            ["Gluten", "Dairy", "Eggs", "Nuts", "Soy", "Sesame"])

    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("Next →", type="primary"):
            st.session_state.preferences_data = {
                'cuisine_type': cuisine_type,
                'meal_type': meal_type,
                'diet_type': diet_type,
                'preferences': preferences,
                'allergens': allergens
            }
            st.session_state.page = "final"
            st.rerun()


def show_metrics_page():
    """Display physical metrics input page"""
    # Create centered container for physical metrics
    st.markdown(
        "<div style='text-align: center; margin: 2rem 0 0 0;'><h1>❤️</h1></div>",
        unsafe_allow_html=True)
    st.markdown("<div class='metrics-container'>", unsafe_allow_html=True)
    st.subheader("Physical Metrics")

    col1, col2 = st.columns(2)
    with col1:
        sex = st.selectbox("Sex", ["Male", "Female"])
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        weight = st.number_input("Weight (kg)",
                                 min_value=20.0,
                                 max_value=300.0,
                                 value=70.0,
                                 step=0.1)
    with col2:
        height = st.number_input("Height (cm)",
                                 min_value=50.0,
                                 max_value=250.0,
                                 value=170.0,
                                 step=0.1)
        activity_level = st.selectbox("Physical Activity Level", [
            "Sedentary", "Lightly Active", "Moderately Active", "Very Active"
        ])

    activity_info = {
        "Sedentary":
        "Minimal physical movement and low exercise. Applies to individuals who spend most of their day sitting or those with limited mobility.",
        "Lightly Active":
        "A person with some physical activity in their daily routine. This includes low-intensity activities such as leisurely walking, light household chores, or casual gardening that amounts to 30-60 minutes of movement per day",
        "Moderately Active":
        "Incorporates physical activity into daily routine, combining movement from daily tasks with planned exercise. Moderate-intensity exercise for about 60-90 minutes most days of the week",
        "Very Active":
        "A very active individual consistently participates in high-intensity or long-duration physical activities, more than 90 minutes a day. Includes occupations requiring significant physical effort."
    }
    st.info(activity_info[activity_level])

    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("Next →", type="primary", key="metrics_next"):
            st.session_state.metrics_data = {
                'sex': sex,
                'age': age,
                'weight': weight,
                'height': height,
                'activity_level': activity_level
            }
            st.session_state.page = "preferences"
            st.rerun()


def show_results_page():
    """Display the results page"""
    form_data = st.session_state.form_data

    # Calculate TDEE and generate recommendations
    targets = calculate_daily_targets(
        weight=form_data['weight'],
        height=form_data['height'],
        age=form_data['age'],
        sex=form_data['sex'],
        activity_level=form_data['activity_level'])

    # Generate summary
    summary = generate_summary(form_data['food_history'])

    # Load recommendations
    foods_df = load_food_data(True, form_data['preferences'],
                              form_data['allergens'],
                              form_data['cuisine_type'],
                              form_data['meal_type'], None, summary,
                              form_data['diet_type'])

    recipes_df = load_recipe_data(True, form_data['preferences'],
                                  form_data['allergens'],
                                  form_data['cuisine_type'],
                                  form_data['meal_type'], summary,
                                  form_data['diet_type'])

    # Display TDEE information
    st.markdown("<h1 style='text-align: center;'>Your Daily Energy Requirements</h1>", unsafe_allow_html=True)
    st.subheader(
        f"Based on your physical metrics and activity level, your Total Daily Energy Expenditure (TDEE) is: **{int(targets['bmr'])} calories**"
    )
    st.subheader(
        "This represents the estimated number of calories you burn each day.")
    st.divider()

    # Display results
    if form_data['display_option'] == "Food Only" and not foods_df.empty:
        st.header("📋 Available Meal Options")
        st.markdown("<h2 style='text-align: center;'>Main Recommendation</h2>", unsafe_allow_html=True)
        main_recommendation = foods_df.iloc[0]
        display_food(main_recommendation, is_openai_mode=True)

    elif form_data['display_option'] == "Recipes Only" and not recipes_df.empty:
        st.header("🥘 Recipes")
        display_recipe(recipes_df.iloc[0], is_openai_mode=True)

    # Add some space and a centered back button
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("← Back to Form", key="back_button"):
            # Clear session state at the start of the next rerun
            st.session_state['clear_on_rerun'] = True
            st.rerun()


def show_final_page():
    """Display final options and generate button"""
    st.markdown(
        "<div style='text-align: center; margin: 2rem 0 0 0;'><h1>🎯</h1></div>",
        unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Final Steps</h3>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    display_option = st.radio("What would you like to see?",
                              ["Food Only", "Recipes Only"],
                              key="display_option")
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("Generate Recommendations", type="primary"):
            metrics_data = st.session_state.metrics_data
            preferences_data = st.session_state.preferences_data
            st.session_state.submitted = True
            st.session_state.form_data = {
                **metrics_data,
                **preferences_data,
                'food_history': st.session_state.food_history,
                'display_option': display_option
            }
            st.rerun()

# Main app logic
if 'clear_on_rerun' in st.session_state and st.session_state.clear_on_rerun:
    # Store submitted state temporarily
    was_submitted = st.session_state.get('submitted', False)
    # Clear all state
    st.session_state.clear()
    # Restore only the submitted state
    st.session_state.submitted = False
elif 'submitted' not in st.session_state:
    st.session_state.submitted = False

if 'page' not in st.session_state:
    st.session_state.page = "welcome"

if st.session_state.submitted:
    show_results_page()
elif st.session_state.page == "welcome":
    show_welcome_page()
elif st.session_state.page == "food_history":
    show_food_history_page()
elif st.session_state.page == "metrics":
    show_metrics_page()
elif st.session_state.page == "preferences":
    show_preferences_page()
elif st.session_state.page == "final":
    show_final_page()