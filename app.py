##############################################################
#                                                            #
#                          MacroAI                           #
#                                                            #
##############################################################

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

chart_data = pd.DataFrame(np.random.randn(10, 4), columns=["weight",'desired_weight',"protein", "carbs"])
df = pd.read_csv('recommended_nutrition_full_cleaned.csv').head(50)

df_food = pd.read_csv('fooddata.csv')

st.title('MacroAI')
st.subheader("AI powered nutritionist")
height = st.sidebar.number_input('Enter your height:', 120, 220, 181)
weight = st.sidebar.number_input('Enter your weight:', 40, 120, 64)
desired_weight = st.sidebar.number_input('Enter your desired weight:', 40, 120, 75)


# Create the line chart
# st.line_chart(df, x="Weight", y=["Protein", "Carbs_max (gram)"], color=["#FFFFFF", "#0000FF"])


# Create a new DataFrame for the line chart
chart_data = df[df["Weight"].between(weight, desired_weight)].copy()

# Add a new column to the chart_data DataFrame for the tooltip
chart_data["foods"] = chart_data["Weight"].apply(lambda x: ', '.join(df_food.sample(3)["Shrt_Desc"].tolist()))

# Create the line chart with tooltips
line_chart = alt.Chart(chart_data).mark_line().encode(
    x="Weight",
    y=alt.Y("Protein", title="Protein"),
    color=alt.value("#0000FF"),
    tooltip=["Weight", "Protein", "foods"]
)

st.altair_chart(line_chart, use_container_width=True)


# Show the dataframe
st.write(df)

st.write(df_food)