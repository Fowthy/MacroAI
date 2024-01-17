import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

# Load the data
df = pd.read_csv('recommended_nutrition_full_cleaned.csv')
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
chart_data = df[df["Weight"].between(weight - 0.5, desired_weight + 0.5)].copy()  # Adjust the range here

# Add a new column to the chart_data DataFrame for the tooltip
def get_foods_and_protein(protein_goal):
    foods = df_food[df_food["Protein_(g)"] > 0].sample(3)  # Ensure that the food has some protein
    food_names = foods["Shrt_Desc"].tolist()
    food_proteins = foods["Protein_(g)"].tolist()  # Protein content per 100g of each food
    food_amounts = [protein_goal * 100 / protein for protein in food_proteins]  # Amount of each food to consume
    return '<br>'.join([f"{name}: {amount:.2f}g, {protein:.2f}g protein/100g" for name, amount, protein in zip(food_names, food_amounts, food_proteins)])

chart_data["foods"] = chart_data["Protein"].apply(get_foods_and_protein)

# Create the line chart with tooltips
fig = px.line(chart_data, x="Weight", y="Protein")
fig.update_traces(hovertemplate='Weight: %{x}kg<br>Protein: %{y}g<br>Foods:<br>%{customdata}', customdata=chart_data['foods'])
st.plotly_chart(fig)

# Prepare the data for training
X = df[['Weight']].values  # Weight
y = df['Protein'].values  # Protein

# Create and train the model
model = LinearRegression()
model.fit(X, y)

# Now you can use the model to predict the protein intake for a given weight
predicted_protein = model.predict([[weight]])
st.write(f'The predicted protein intake for a weight of {weight} kg is {predicted_protein[0]} g.')

# Show the dataframes
st.write(df)
st.write(df_food)