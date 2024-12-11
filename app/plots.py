import streamlit as st
import plotly.express as px

def plot_agency_counts(df):
    bid_counts = df['Agency/Department'].value_counts().reset_index()
    bid_counts.columns = ['Agency/Department', 'Bid Count']
    fig = px.bar(bid_counts, x='Agency/Department', y='Bid Count', title='Bids by Customer')
    st.plotly_chart(fig)

def plot_bids_time(df):
    df['Month'] = df['Date Bid Submitted'].dt.month
    df['Year'] = df['Date Bid Submitted'].dt.year
    # Group the data by month and count the number of bids
    monthly_bids_year = df.groupby('Month')['Date Bid Submitted'].count().reset_index()
    monthly_bids_year.columns = ['Month', 'Monthly Bids']
    # Calculate the cumulative sum of bids
    monthly_bids_year['Cumulative Bids'] = monthly_bids_year['Monthly Bids'].cumsum() 
    fig = px.line(monthly_bids_year, x='Month', y=['Monthly Bids', 'Cumulative Bids'], title='Bids by Month')
    st.plotly_chart(fig)

def plot_brand_pie(df):
    manufacturer_counts = df['Manufacturer'].value_counts().reset_index()
    manufacturer_counts.columns = ['Manufacturer', 'Bid Count']
    fig = px.pie(manufacturer_counts, values='Bid Count', names='Manufacturer', title='Manufacturer Distribution')
    st.plotly_chart(fig)
