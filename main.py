import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    file_path = 'europe_df_2.csv'  # Ensure correct path
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Ensure necessary columns exist
if 'Country' not in df.columns or 'Year' not in df.columns:
    st.error("Dataset must contain 'Country' and 'Year' columns.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect("Select Countries", df['Country'].unique(), default=df['Country'].unique())
min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# Filter Data
df_filtered = df[df['Country'].isin(selected_countries)]
df_filtered = df_filtered[(df_filtered['Year'] >= year_range[0]) & (df_filtered['Year'] <= year_range[1])]

# Main Dashboard
st.title("Interactive Economic Dashboard")
st.markdown("Select columns to visualize their relationship.")

# Column Selection
numeric_columns = df_filtered.select_dtypes(include=['number']).columns
x_col = st.selectbox("Select X-axis Column", numeric_columns)
y_col = st.selectbox("Select Y-axis Column", numeric_columns)
plot_type = st.selectbox("Select Plot Type", ['Scatter', 'Line', 'Bar'])

# Plot Data
if x_col and y_col:
    if plot_type == 'Scatter':
        fig = px.scatter(df_filtered, x=x_col, y=y_col, color='Country', title=f'{x_col} vs {y_col}')
    elif plot_type == 'Line':
        fig = px.line(df_filtered, x='Year', y=y_col, color='Country', title=f'{y_col} over Years')
    elif plot_type == 'Bar':
        fig = px.bar(df_filtered, x='Country', y=y_col, color='Country', title=f'{y_col} by Country')
    
    st.plotly_chart(fig)
else:
    st.warning("Please select valid columns to visualize.")
