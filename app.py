import streamlit as st
import pandas as pd
import plotly.express as px

# App config
st.set_page_config(page_title="Car Price Visualizer", layout="wide")

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("CARS.csv")
    df['MSRP'] = df['MSRP'].replace('[$,]', '', regex=True).astype('int64')
    df['Invoice'] = df['Invoice'].replace('[$,]', '', regex=True).astype('int64')
    return df

df = load_data()

# Sidebar: Filter section
st.sidebar.title("🔍 Filter Options")

# Car Type
car_type = st.sidebar.selectbox("Select Car Type", sorted(df['Type'].unique()))
filtered_df = df[df['Type'] == car_type]

# Make
make = st.sidebar.selectbox("Select Car Make", sorted(filtered_df['Make'].unique()))
filtered_df = filtered_df[filtered_df['Make'] == make]

# Model (multi-select)
models = sorted(filtered_df['Model'].unique())
selected_models = st.sidebar.multiselect("Select Car Models", models, default=models)

# Filter based on models
filtered_df = filtered_df[filtered_df['Model'].isin(selected_models)]

# MSRP and Invoice range filters
min_price = int(df['MSRP'].min())
max_price = int(df['MSRP'].max())
price_range = st.sidebar.slider("Filter by MSRP Price Range", min_price, max_price, (min_price, max_price))
filtered_df = filtered_df[(filtered_df['MSRP'] >= price_range[0]) & (filtered_df['MSRP'] <= price_range[1])]

invoice_range = st.sidebar.slider("Filter by Invoice Range", int(df['Invoice'].min()), int(df['Invoice'].max()), 
                                  (int(df['Invoice'].min()), int(df['Invoice'].max())))
filtered_df = filtered_df[(filtered_df['Invoice'] >= invoice_range[0]) & (filtered_df['Invoice'] <= invoice_range[1])]

# Main title
st.title("🚗 Car Price Visualizer Dashboard")

# Metrics
col1, col2 = st.columns(2)
col1.metric("🔷 Avg MSRP", f"${filtered_df['MSRP'].mean():,.0f}")
col2.metric("🟢 Avg Invoice", f"${filtered_df['Invoice'].mean():,.0f}")

# Chart selector
st.subheader("📊 Chart Customization")
chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot"])
price_choice = st.radio("Select Price Type", ["MSRP", "Invoice", "Both"], horizontal=True)

# Display chart
def show_chart(df):
    if chart_type == "Bar Chart":
        if price_choice == "Both":
            df_melted = df.melt(id_vars='Model', value_vars=['MSRP', 'Invoice'])
            fig = px.bar(df_melted, x='Model', y='value', color='variable', barmode='group',
                         labels={'value': 'Price ($)', 'variable': 'Price Type'})
        else:
            fig = px.bar(df, x='Model', y=price_choice, color='Model',
                         labels={price_choice: 'Price ($)'})
    elif chart_type == "Line Chart":
        if price_choice == "Both":
            df_melted = df.melt(id_vars='Model', value_vars=['MSRP', 'Invoice'])
            fig = px.line(df_melted, x='Model', y='value', color='variable', markers=True,
                          labels={'value': 'Price ($)', 'variable': 'Price Type'})
        else:
            fig = px.line(df, x='Model', y=price_choice, markers=True, color='Model',
                          labels={price_choice: 'Price ($)'})
    elif chart_type == "Scatter Plot":
        fig = px.scatter(df, x='Invoice', y='MSRP', color='Model', size='MSRP',
                         hover_name='Model', labels={'Invoice': 'Invoice Price ($)', 'MSRP': 'MSRP Price ($)'})
    elif chart_type == "Box Plot":
        df_melted = df.melt(id_vars='Model', value_vars=['MSRP', 'Invoice'])
        fig = px.box(df_melted, x='variable', y='value', color='variable',
                     labels={'value': 'Price ($)', 'variable': 'Price Type'})
    else:
        fig = px.bar(df, x='Model', y='MSRP')

    fig.update_layout(xaxis_tickangle=-45)
    return fig

if not filtered_df.empty:
    st.plotly_chart(show_chart(filtered_df), use_container_width=True)
else:
    st.warning("No data matches the selected filters. Please adjust your selections.")

# Optional: Show data table
with st.expander("📄 View Filtered Data Table"):
    st.dataframe(filtered_df)

# Download option
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Filtered Data as CSV", csv, "filtered_cars.csv", "text/csv")

# Footer
st.markdown("---")
st.markdown("✅ Built with ❤️ using Streamlit | Source: `CARS.csv` dataset")
