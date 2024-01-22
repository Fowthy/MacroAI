import streamlit as st
import pandas as pd

# Load the data
df_food = pd.read_csv('./fooddata.csv').head(100)

# User inputs
search_term = st.text_input('Search for a food item:')

# Filter the food items
filtered_food = df_food[df_food['Shrt_Desc'].str.contains(search_term, case=False, na=False)]

# Display the food items in a grid
cols = st.columns(3)
selected_foods = []
for i, food in enumerate(filtered_food['Shrt_Desc']):
    if cols[i % 3].checkbox(food):
        selected_foods.append(food)

# Display the selected food items
st.write('You selected:')
for food in selected_foods:
    st.write(food)