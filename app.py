import streamlit as st
import pandas as pd
import plotly.express as px

# App title and layout
st.set_page_config(page_title="Car Price Visualizer", layout="wide")

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("CARS.csv")
    df['MSRP'] = df['MSRP'].replace('[$,]', '', regex=True).astype('int64')
    df['Invoice'] = df['Invoice'].replace('[$,]', '', regex=True).astype('int64')
    return df

df = load_data()

# Sidebar for filters
st.sidebar.header("🔍 Filter Options")

car_type = st.sidebar.selectbox("Select Car Type", sorted(df['Type'].unique()))
filtered_df = df[df['Type'] == car_type]

make = st.sidebar.selectbox("Select Car Make", sorted(filtered_df['Make'].unique()))
final_df = filtered_df[filtered_df['Make'] == make]

# Optional: model selection (multi-select)
models = final_df['Model'].unique()
selected_models = st.sidebar.multiselect("Select Models", models, default=models)

plot_df = final_df[final_df['Model'].isin(selected_models)]

# Main area
st.title("🚗 Car MSRP & Invoice Visualizer")

# Show summary metrics
col1, col2 = st.columns(2)
col1.metric("Average MSRP", f"${plot_df['MSRP'].mean():,.0f}")
col2.metric("Average Invoice", f"${plot_df['Invoice'].mean():,.0f}")

# Chart type selection
chart_type = st.radio("Choose Chart Type:", ["MSRP Only", "MSRP vs Invoice"], horizontal=True)

# Plot chart
if chart_type == "MSRP Only":
    fig = px.bar(plot_df, x='Model', y='MSRP', color='Model',
                 title=f"MSRP of {make} Models ({car_type} Type)",
                 labels={'MSRP': 'Price ($)'})
else:
    fig = px.bar(plot_df.melt(id_vars=['Model'], value_vars=['MSRP', 'Invoice']),
                 x='Model', y='value', color='variable', barmode='group',
                 title=f"MSRP vs Invoice for {make} Models ({car_type} Type)",
                 labels={'value': 'Price ($)', 'variable': 'Price Type'})

fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

# Optional: Show data table
with st.expander("📄 Show Data Table"):
    st.dataframe(plot_df)

# Download option
csv = plot_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Filtered Data as CSV", csv, "filtered_cars.csv", "text/csv")


