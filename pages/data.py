import streamlit as st
import pandas as pd

df = pd.read_csv('recommended_nutrition_full_cleaned.csv')
df_food = pd.read_csv('fooddata.csv')

st.write("This is the dataframe with the recommended nutrition value for different weights")
st.dataframe(df)
st.write("This is the dataframe with the foods data and their nutrition content")
st.dataframe(df_food)