##############################################################
#                                                            #
#                          MacroAI                           #
#                                                            #
##############################################################

import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(np.random.randn(10, 3), columns=["weight",'desired_weight',"protein", "carbs"])

st.title('MacroAI')
st.subheader("AI powered nutritionist")
height = st.sidebar.text_area('Enter your height:')
weight = st.sidebar.text_area('Enter your weight:')
desired_weight = st.sidebar.slider('Select desired weight', 50, 200, 64)


st.line_chart(
   chart_data, x="desired_weight", y=["protein", "carbs"], color=["#FFFFFF", "#0000FF"]  # Optional
)

