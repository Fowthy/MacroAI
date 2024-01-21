import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Load the data
df = pd.read_csv('recommended_nutrition_full_cleaned.csv')
df_food = pd.read_csv('fooddata.csv')

# Convert 'Weight' from pounds to kilograms
df["Weight"] = df["Weight"] / 2.20462

# Remove duplicates where 'Weight' is the same
df = df.loc[~df.duplicated(subset='Weight')]

# User inputs
height = st.sidebar.number_input('Enter your height:', 120, 220, 181)
weight = st.sidebar.number_input('Enter your weight:', 40, 120, 64)
age = st.sidebar.number_input('Enter your age:', 18, 80, 30)
activity_level = st.sidebar.selectbox('Select your activity level:', ['Sedentary', 'Lightly active', 'Moderately active', 'Very active', 'Extra active'])
activity_level_map = {
    'Sedentary': 1.2,
    'Lightly active': 1.375,
    'Moderately active': 1.55,
    'Very active': 1.725,
    'Extra active': 1.9
}

st.title('MacroAI')
st.subheader("AI powered nutritionist")


# Prepare the data for training
features = ['Weight', 'Height', 'Age']
target = ['Protein', 'Carbs_max (gram)', 'Fat_max (gram)']

X = df[features]  # Features
y = df[target]  # Target variables

# Create and train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Now you can use the model to predict the nutritional intake for a given weight, height, age, and activity level
predicted_nutrition = model.predict([[weight, height, age]])
st.write(f'The predicted nutritional intake for a weight of {weight} kg, height of {height} cm, age of {age} years, and activity level "{activity_level}" is:')
st.write(f'Protein: {predicted_nutrition[0][0]} g')
st.write(f'Carbs: {predicted_nutrition[0][1]} g')
st.write(f'Fat: {predicted_nutrition[0][2]} g')

# Predict weight change over time
weeks = range(1, 13)  # Weeks 1 to 12
predicted_weights = [weight - model.predict([[weight, height, age]])[0][0] * week / 7 for week in weeks]
desired_weight = st.sidebar.number_input('Enter your desired weight:', 40, 120, 78)

# Create a new DataFrame for the line chart
chart_data = df[df["Weight"].between(weight - 2, desired_weight + 2)].copy()  # Adjust the range here

# Add a new column to the chart_data DataFrame for the tooltip
def get_foods_and_protein(protein_goal):
    foods = df_food[df_food["Protein_(g)"] > 0].sample(3)  # Ensure that the food has some protein
    food_names = foods["Shrt_Desc"].tolist()
    food_proteins = foods["Protein_(g)"].tolist()  # Protein content per 100g of each food
    food_amounts = [protein_goal * 100 / protein for protein in food_proteins]  # Amount of each food to consume
    return '<br>'.join([f"{name}: {amount:.2f}g, {protein:.2f}g protein/100g" for name, amount, protein in zip(food_names, food_amounts, food_proteins)])

chart_data["foods"] = chart_data["Protein"].apply(get_foods_and_protein)

# Add a new column for the legend
chart_data["Legend"] = "Protein Intake"

# Create the line chart with tooltips
fig = px.line(chart_data, x="Weight", y="Protein", color="Legend")
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

