import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
import plotly.graph_objects as go


# Load the data
df = pd.read_csv('recommended_nutrition_full_cleaned.csv')
df_food = pd.read_csv('fooddata.csv')

# Convert 'Weight' from pounds to kilograms
df["Weight"] = df["Weight"] / 2.20462

# Remove duplicates where 'Weight' is the same
df = df.loc[~df.duplicated(subset='Weight')]

# User inputs
height = st.sidebar.number_input('Enter your height:', 120, 220, 192)
weight = st.sidebar.number_input('Enter your weight:', 40, 120, 68)
# desired_weight = st.sidebar.number_input('Enter your desired weight:', 40, 120, 78)
age = st.sidebar.number_input('Enter your age:', 18, 80, 30)
activity_level = st.sidebar.selectbox('Select your activity level:', ['Sedentary', 'Lightly active', 'Moderately active', 'Very active', 'Extra active'])
goal = st.sidebar.radio('Select your goal:', ['Gain weight'])
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

X = df[features]
y = df[target] 

# Create and train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

def predict_nutrition(weight, height, age):
    # Use the trained model to predict the nutritional intake
    predicted_nutrition = model.predict([[weight, height, age]])
    return predicted_nutrition

# Now you can use the function to predict the nutritional intake for a given weight, height, and age
predicted_nutrition = predict_nutrition(weight, height, age)
st.markdown(f'The predicted nutritional intake for a weight of **{weight} kg**, height of **{height} cm**, age of **{age} years**, and activity level "**{activity_level}**" is:')
st.markdown(f'**Protein**: <span style="color:blue">{predicted_nutrition[0][0]} g</span>', unsafe_allow_html=True)
st.markdown(f'**Carbs**: <span style="color:green">{predicted_nutrition[0][1]} g</span>', unsafe_allow_html=True)
st.markdown(f'**Fat**: <span style="color:red">{predicted_nutrition[0][2]} g</span>', unsafe_allow_html=True)

healthy_weight = 21.75 * (height / 100) ** 2  # Healthy weight based on BMI

st.write(f'Your healthy weight is {healthy_weight:.2f} kg')

# Create a new DataFrame for the line chart
chart_data = df[df["Weight"].between(weight - 2, healthy_weight)].copy()  # Adjust the range here

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

fig = go.Figure()

nutrients = ['Protein', 'Carbs_max (gram)', 'Fat_max (gram)']
selected_nutrients = st.multiselect('Select nutrients:', nutrients, default=nutrients)

for nutrient in selected_nutrients:
    fig.add_trace(go.Scatter(x=chart_data["Age"], y=chart_data[nutrient], mode='lines', name=nutrient,
                             hovertemplate='Weight: %{x}kg<br>'+nutrient+': %{y}g<br>Foods:<br>%{customdata}',
                             customdata=chart_data['foods']))

fig.update_layout(title='Nutrient Intake vs Weight', xaxis_title='Weight (kg)', yaxis_title='Nutrient Intake (g)')
st.plotly_chart(fig)