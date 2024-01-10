##############################################################
#                                                            #
#                          MacroAI                           #
#                                                            #
##############################################################

import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["weight", "protein", "carbs"])

st.title('MacroAI')
st.form_sutitle("AI powered nutritionist")
height = st.text_area('Enter your height:')
weight = st.text_area('Enter your weight:')
desired_weight = st.text_area('Enter your desired weight:')

st.line_chart(
   chart_data, x="protein", y=["protein", "carbs"], color=["#FF0000", "#0000FF"]  # Optional
)

