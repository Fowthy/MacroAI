##############################################################
#                                                            #
#                          MacroAI                           #
#                                                            #
##############################################################

import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv('recommended_nutrition_full_cleaned.csv').head(50)
df_food = pd.read_csv('fooddata.csv')

# User inputs
st.title('MacroAI')
st.subheader("AI powered nutritionist")
height = st.sidebar.number_input('Enter your height:', 120, 220, 181)
weight = st.sidebar.number_input('Enter your weight:', 40, 120, 64) * 2.20462  # Convert weight to pounds
desired_weight = st.sidebar.number_input('Enter your desired weight:', 40, 120, 75) * 2.20462  # Convert desired weight to pounds


# Create the line chart
# st.line_chart(df, x="Weight", y=["Protein", "Carbs_max (gram)"], color=["#FFFFFF", "#0000FF"])


# Create a new DataFrame for the line chart
chart_data = df[df["Weight"].between(weight, desired_weight)].copy()

# Add a new column to the chart_data DataFrame for the tooltip
chart_data["foods"] = chart_data["Weight"].apply(lambda x: ', '.join(df_food.sample(3)["Shrt_Desc"].tolist()))


# Create the line chart with tooltips
fig = px.line(chart_data, x="Weight", y="Protein", hover_data=["foods"])
st.plotly_chart(fig)




# Show the dataframe
st.write(df)

st.write(df_food)

st.write(chart_data)