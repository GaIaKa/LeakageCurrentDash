import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import gdown

# Set page configuration
st.set_page_config(page_title="PG Measurements in Magdeburg", page_icon="☀️", layout="wide")

# Function to download and load data from Google Drive
@st.cache_data
def load_data(file_id):
    try:
        # Download file using gdown
        output = 'data.csv'
        gdown.download(f'https://drive.google.com/uc?id={file_id}', output, quiet=False)
        
        # Load the CSV file
        df = pd.read_csv(output)
        df['timestamp'] = pd.to_datetime(df['timestamp'])  # Ensure 'timestamp' is datetime type
        return df
    except Exception as e:
        st.write("Error reading the data:", e)
        return None

# Direct Google Drive file ID (replace with yours)
file_id = '1unB6AcgZNH9eO6XeqSFy5PSAfMcluta6'
data = load_data(file_id)

# Check if data is loaded
if data is not None:
    st.write("Data successfully loaded!")
else:
    st.write("Failed to load data.")

# Default date range: Last month in the data
latest_date = data['timestamp'].max()
default_start_date = latest_date - timedelta(days=30)

# Sidebar for Date Range Picker
st.sidebar.header("Select Date Range")
start_date, end_date = st.sidebar.date_input(
    "Select date range:",
    value=[default_start_date, latest_date],
    min_value=data['timestamp'].min().date(),
    max_value=data['timestamp'].max().date()
)

# Sidebar for Variable Selection (Checkboxes)
st.sidebar.header("Select Variables to Plot")
plot_efield = st.sidebar.checkbox('Efield', value=True)  # Default to True (checked)
plot_currna = st.sidebar.checkbox('curr-na', value=True)  # Default to True (checked)
plot_interrh = st.sidebar.checkbox('interRH', value=True)  # Default to True (checked)
plot_tempdeg = st.sidebar.checkbox('tempdeg', value=True)  # Default to True (checked)

# Filter data based on selected date range
filtered_data = data[(data['timestamp'] >= pd.to_datetime(start_date)) & (data['timestamp'] <= pd.to_datetime(end_date))]

# Create Plotly figure for Page 2
if not filtered_data.empty:
    fig = go.Figure()

    # Plot Efield if selected
    if plot_efield:
        fig.add_trace(go.Scatter(
            x=filtered_data['timestamp'], 
            y=filtered_data['Efield'], 
            mode='lines', 
            name='Electric Field',
            line=dict(color='royalblue', width=2),
            yaxis='y1'
        ))

    # Plot curr-na if selected
    if plot_currna:
        fig.add_trace(go.Scatter(
            x=filtered_data['timestamp'], 
            y=filtered_data['curr-na'], 
            mode='lines', 
            name='Leakage Current',
            line=dict(color='crimson', width=2),
            yaxis='y2'
        ))

    # Plot interRH if selected
    if plot_interrh:
        fig.add_trace(go.Scatter(
            x=filtered_data['timestamp'], 
            y=filtered_data['interRH'], 
            mode='lines', 
            name='Relative Humidity',
            line=dict(color='green', width=2),
            yaxis='y3'
        ))

    # Plot tempdeg if selected
    if plot_tempdeg:
        fig.add_trace(go.Scatter(
            x=filtered_data['timestamp'], 
            y=filtered_data['tempdeg'], 
            mode='lines', 
            name='Temperature (°C)',
            line=dict(color='orange', width=2),
            yaxis='y4'
        ))

    # Update layout with four different y-axes
    fig.update_layout(
        title=f"PG Measurements from {start_date} to {end_date}",
        xaxis_title='Timestamp',
        xaxis=dict(
            showgrid=True,
            linecolor='black',
            linewidth=1,
            tickangle=-45, 
            tickfont=dict(size=16)
        ),
        yaxis=dict(
            title='Electric Field (V/m)',
            titlefont=dict(color='royalblue'),
            tickfont=dict(color='royalblue'),
            showgrid=True,
            linecolor='black',
            linewidth=1,
        ),
        yaxis2=dict(
            title='Leakage Current',
            titlefont=dict(color='crimson'),
            tickfont=dict(color='crimson'),
            linecolor='black',
            linewidth=1,
            overlaying='y',
            side='right',
            showgrid=True,
        ),
        yaxis3=dict(
            title='Relative Humidity (%)',
            titlefont=dict(color='green'),
            tickfont=dict(color='green'),
            linecolor='black',
            linewidth=1,
            overlaying='y',
            side='right',
            position=0.85,
            showgrid=True,
        ),
        yaxis4=dict(
            title='Temperature (°C)',
            titlefont=dict(color='orange'),
            tickfont=dict(color='orange'),
            linecolor='black',
            linewidth=1,
            overlaying='y',
            side='right',
            position=0.9,
            showgrid=True,
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial', size=14, color='Black'),
        hovermode='x',
        height=600,
        width=1100
    )

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data available for the selected date range.")
