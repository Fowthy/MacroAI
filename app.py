import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load the data
df = pd.read_csv('recommended_nutrition_full_cleaned.csv').head(50)
df_food = pd.read_csv('fooddata.csv')

# Convert 'Weight' from pounds to kilograms
df["Weight"] = df["Weight"] / 2.20462

# User inputs
st.title('MacroAI')
st.subheader("AI powered nutritionist")
height = st.sidebar.number_input('Enter your height:', 120, 220, 181)
weight = st.sidebar.number_input('Enter your weight:', 40, 120, 64)
desired_weight = st.sidebar.number_input('Enter your desired weight:', 40, 120, 75)

# Create a new DataFrame for the line chart
chart_data = df[df["Weight"].between(weight, desired_weight)].copy()

# Add a new column to the chart_data DataFrame for the tooltip
def get_foods_and_protein(protein_goal):
    foods = df_food.sample(3)
    food_names = foods["Shrt_Desc"].tolist()
    food_proteins = foods["Protein_(g)"].tolist()  # Protein content per 100g of each food
    food_amounts = [protein_goal * 100 / protein for protein in food_proteins]  # Amount of each food to consume
    return '<br>'.join([f"{name}: {amount:.2f}g, {protein:.2f}g protein/100g" for name, amount, protein in zip(food_names, food_amounts, food_proteins)])

chart_data["foods"] = chart_data["Protein"].apply(get_foods_and_protein)

# Create the line chart with tooltips
fig = px.line(chart_data, x="Weight", y="Protein")
fig.update_traces(hovertemplate='Weight: %{x}kg<br>Protein: %{y}g<br>Foods:<br>%{customdata}', customdata=chart_data['foods'])
st.plotly_chart(fig)

# Show the dataframes
st.write(df)
st.write(df_food)