##############################################################
#                                                            #
#                          MacroAI                           #
#                                                            #
##############################################################

import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(np.random.randn(10, 100), columns=["weight", "protein", "carbs"])

st.title('MacroAI')
st.subheader("AI powered nutritionist")
height = st.text_area('Enter your height:')
weight = st.text_area('Enter your weight:')
desired_weight = st.sidebar.slider('Select desired weight', 50, 200, 64)


st.line_chart(
   chart_data, x="protein", y=["protein", "carbs"], color=["#FFFFFF", "#0000FF"]  # Optional
)

