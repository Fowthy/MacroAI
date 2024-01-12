##############################################################
#                                                            #
#                          MacroAI                           #
#                                                            #
##############################################################

import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(np.random.randn(10, 4), columns=["weight",'desired_weight',"protein", "carbs"])
df = pd.read_csv('recommended_nutrition_full_cleaned.csv')

st.title('MacroAI')
st.subheader("AI powered nutritionist")
height = st.sidebar.text_area('Enter your height:')
weight = st.sidebar.text_area('Enter your weight:')
desired_weight = st.sidebar.slider('Select desired weight', 50, 200, 64)


st.line_chart(
   chart_data, x="desired_weight", y=["protein", "carbs"], color=["#FFFFFF", "#0000FF"]  # Optional
)

# Create the line chart
st.line_chart(df, x="Weight", y=["Protein", "Carbs"], color=["#FFFFFF", "#0000FF"]  # Optional)


# Show the dataframe
st.write(df)