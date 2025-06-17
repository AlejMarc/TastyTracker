import streamlit as st
import pandas as pd
import json
from utils.openai_helper import analyze_recipe, suggest_recipes, explain_food
from utils.api_data import get_recipe_cook_time

def display_food(food, is_openai_mode=False):
    #Display a food item with nutritional info and analysis
    try:
        # Handle potential JSON string and raw response
        if isinstance(food, pd.Series) and 'raw_response' in food:
            try:
                raw_response = food['raw_response'].strip()
                # st.write("Debug - Raw Response:", raw_response)  # Debug line
                # Clean the response
                raw_response = raw_response.replace('\n', ' ').replace('\r', '')
                parsed_food = json.loads(raw_response)
                # Handle nested structure if present
                if 'food_item' in parsed_food:
                    food = parsed_food['food_item']
                else:
                    food = parsed_food
            except json.JSONDecodeError as e:
                st.error(f"Could not parse food data: {str(e)}")
                st.write("Problematic JSON:", raw_response)  # Show the problematic JSON
                return
        elif isinstance(food, str):
            try:
                raw_response = food.strip()
                st.write("Debug - Raw Response:", raw_response)  # Debug line
                # Clean the response
                raw_response = raw_response.replace('\n', ' ').replace('\r', '')
                food = json.loads(raw_response)
            except json.JSONDecodeError as e:
                st.error(f"Could not parse food data: {str(e)}")
                st.write("Problematic JSON:", raw_response)  # Show the problematic JSON
                return

        # Extract individual fields for display
        name = food.get('name', 'N/A')
        description = food.get('description', 'N/A')
        cuisine_type = food.get('cuisine_type', 'N/A')
        meal_type = food.get('meal_type', 'N/A')
        dietary_info = food.get('dietary_info', 'N/A')
        if isinstance(dietary_info, dict):
            string_representation_formatted = ', '.join(f'{key}: {value}' for key, value in dietary_info.items())
            dietary_info = string_representation_formatted
        allergens = food.get('allergens', 'N/A')
        calories = food.get('calories', 'N/A')
        protein = food.get('protein', 'N/A')
        carbs = food.get('carbs', 'N/A')
        fat = food.get('fat', 'N/A')

        # Display food name
        st.markdown(f"<h2 style='text-align: center;'>{name}</h2>", unsafe_allow_html=True)

        # Get actual nutritional data from API
        from utils.api_data import get_nutritional_info
        nutrition_data = get_nutritional_info(name)

        # Food type info
        st.markdown(f"**Cuisine:** {cuisine_type}")
        st.markdown(f"**Meal Type:** {meal_type}")

        # Show food description
        if 'description' in food and food['description'] != 'N/A':
            st.write(description)


        if 'dietary_info' in food and food['dietary_info'] not in ['None', 'N/A']:
            st.markdown("**Dietary Information:** " + str(dietary_info))
        else:
            st.markdown("**Dietary_info:** None declared")


        if 'allergens' in food and food['allergens'] not in ['None', 'N/A']:
            st.markdown("**Contains allergens:** " + str(allergens))
        else:
            st.markdown("**Allergens:** None declared")

        # Display nutritional information from API
        st.markdown("<h3 style='text-align: center;'>Nutritional Information</h3>", unsafe_allow_html=True)
        if "error" not in nutrition_data:
            # Display food image if available
            if nutrition_data.get('image'):
                st.markdown("""
                    <div style='display: flex; justify-content: center; align-items: center; margin: 2rem 0;'>
                        <div style='max-width: 400px; width: 100%; text-align: center;'>
                """, unsafe_allow_html=True)
                st.image(nutrition_data['image'], caption=name, use_container_width=True)
                st.markdown("</div></div>", unsafe_allow_html=True)

            col_nut1, col_nut2, col_nut3, col_nut4 = st.columns(4)
            with col_nut1:
                st.metric("Calories", nutrition_data['calories'])
            with col_nut2:
                st.metric("Protein", f"{nutrition_data['protein']}g")
            with col_nut3:
                st.metric("Carbs", f"{nutrition_data['carbs']}g")
            with col_nut4:
                st.metric("Fat", f"{nutrition_data['fat']}g")
        else:
            st.warning("Could not fetch nutritional information from API")

        # Build nutritional text for analysis
        nutritional_info = f"""
        - Calories: {food['calories']}
        - Protein: {food['protein']}g
        - Carbs: {food['carbs']}g
        - Fat: {food['fat']}g
        """

        # Generate or show AI-powered insights
        st.markdown("<h3 style='text-align: center;'>Insights</h3>", unsafe_allow_html=True)

        # Generate food explanation with OpenAI
        with st.spinner("Generating analysis..."):
            food_explanation = explain_food(
                food['name'], 
                nutritional_info, 
                food['description'] if 'description' in food else ""
            )

        if food_explanation:
            st.markdown(food_explanation)
        else:
            st.info("Analysis not available.")

    except Exception as e:
        st.error(f"Error displaying food: {str(e)}")


def display_recipe(recipe, is_openai_mode=False):
    # Display a recipe with ingredients, instructions and analysis
    # Display recipe name
    st.markdown(f"<h2 style='text-align: center;'>{recipe['name']}</h2>", unsafe_allow_html=True)

    # Display recipe info
    # Recipe metadata
    st.markdown(f"**Cuisine:** {recipe['cuisine_type']}")
    st.markdown(f"**Meal Type:** {recipe['meal_type']}")
    st.markdown(f"**Dietary Info:** {recipe['dietary_info']}")

    # Get nutritional information from API
    from utils.api_data import get_nutritional_info
    nutrition_data = get_nutritional_info(recipe['name'])

    # Display nutritional information
    st.markdown("<h3 style='text-align: center;'>Nutritional Information</h3>", unsafe_allow_html=True)
    if "error" not in nutrition_data:
        # Display food image if available
        if nutrition_data.get('image'):
            st.image(nutrition_data['image'], caption=recipe['name'])

        col_nut1, col_nut2, col_nut3, col_nut4 = st.columns(4)
        with col_nut1:
            st.metric("Calories", nutrition_data['calories'])
        with col_nut2:
            st.metric("Protein", f"{nutrition_data['protein']}g")
        with col_nut3:
            st.metric("Carbs", f"{nutrition_data['carbs']}g")
        with col_nut4:
            st.metric("Fat", f"{nutrition_data['fat']}g")
    else:
        st.warning("Could not fetch nutritional information from API")

    if recipe['allergens'] not in ['None', 'N/A']:
        st.markdown(f"**Contains allergens:** {recipe['allergens']}")
    else:
        st.markdown("**Allergens:** None declared")

    # Recipe details
    time_col1, time_col2 = st.columns(2)

    # Try to get Spoonacular cooking time
    spoonacular_time = get_recipe_cook_time(recipe['name'])

    # Display Spoonacular API response
    if spoonacular_time:
        st.info(f"Spoonacular API suggests {spoonacular_time} minutes total cooking time for this recipe.")
    # else:
    #     st.warning("Could not verify cooking time from Spoonacular API")

    with time_col1:
        prep_time = recipe['prep_time'] if recipe['prep_time'] != 'N/A' else 'N/A'
        st.metric("Prep Time", f"{prep_time} mins" if prep_time != 'N/A' else 'N/A')
    with time_col2:
        # Use Spoonacular time if available, otherwise fall back to recipe time
        cooking_time = spoonacular_time if spoonacular_time is not None else recipe['cooking_time']
        cooking_time = 'N/A' if cooking_time in ['N/A', None] else cooking_time
        st.metric("Total Cook Time", f"{cooking_time} mins" if cooking_time != 'N/A' else 'N/A')

    # Ingredients
    st.markdown("<h3 style='text-align: center;'>Ingredients</h3>", unsafe_allow_html=True)
    ingredients = recipe['ingredients']
    if isinstance(ingredients, str):
        if '|' in ingredients:
            ingredients_list = ingredients.split('|')
            st.write(', '.join(i.strip() for i in ingredients_list))
        else:
            st.write(ingredients)
    else:
        st.write(ingredients)

    # Instructions
    st.markdown("<h3 style='text-align: center;'>Instructions</h3>", unsafe_allow_html=True)
    instructions = recipe['instructions'] 
    if isinstance(instructions, str):
        if '|' in instructions:
            steps = instructions.split('|')
            st.write(' '.join(f"{step.strip()}. " for step in steps))
        else:
            st.write(instructions)
    else:
        st.write(instructions)

    # Analysis and suggestions
    st.markdown("<h3 style='text-align: center;'>Recipe Analysis</h3>", unsafe_allow_html=True)
    with st.spinner("Analyzing recipe..."):
        analysis = analyze_recipe(
            recipe['name'],
            recipe['ingredients'],
            recipe['instructions']
        )
        if analysis:
            st.markdown(analysis)
        else:
            st.info("Analysis not available.")


