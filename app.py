import streamlit as st
import pandas as pd
import plotly.express as px

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("CARS.csv")
    df['MSRP'] = df['MSRP'].replace('[$,]', '', regex=True).astype('int64')
    df['Invoice'] = df['Invoice'].replace('[$,]', '', regex=True).astype('int64')
    return df

df = load_data()

st.title("Car MSRP Visualizer")

# Dropdown to select car Type
car_type = st.selectbox("Select Car Type", sorted(df['Type'].unique()))

# Filter dataframe based on selected Type
filtered_df = df[df['Type'] == car_type]

# Dropdown to select Make based on selected Type
make = st.selectbox("Select Make", sorted(filtered_df['Make'].unique()))

# Final filtered dataframe
final_df = filtered_df[filtered_df['Make'] == make]

# Display bar chart using Plotly
fig = px.bar(final_df, x='Model', y='MSRP', color='Model',
             title=f"MSRP of {make} Models ({car_type} Type)",
             labels={'MSRP': 'Price ($)'})
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# Optional: Show data table
if st.checkbox("Show Data Table"):
    st.dataframe(final_df)
