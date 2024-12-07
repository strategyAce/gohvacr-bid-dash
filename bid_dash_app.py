import streamlit as st
import pandas as pd
from app.plots import plot_agency_counts, plot_bids_time, plot_brand_pie
from app.auth import authenticate

# Constants
BANNER_PATH = "StratAceBanner_Logo.png"
LOGO_PATH = "gohvacrsupply_logo.svg"
DATA_PATH = 'data/GOHVACRSUPPLY Bid Tracker.csv'
url = "https://strategyace.win/"

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.image(BANNER_PATH,width=None)
        st.subheader(" ")
        st.title("Login to Bid Dashboard")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                st.success("Login successful!")
                st.session_state.logged_in = True
            else:
                st.error("Invalid username or password.")
    else:
        st.image(LOGO_PATH,width=700)
        st.write(" ")
        st.title("FY2024 Government Bid Dashboard")
        st.divider()
        
        #Input correct fiscal year value to display
        fiscal_year = 2024   #<- Update this value
        
        #Read in latest CSV File Data
        df = pd.read_csv(DATA_PATH)
        #Convert Dates to the right format
        df['Date Bid Submitted'] = pd.to_datetime(df['Date Bid Submitted'], format='%m/%d/%Y', errors='coerce')
        #Filter out entries without submission dates
        filtered_df = df[pd.notnull(df['Date Bid Submitted'])]
        #filter for correct fiscal year
        filtered_df = filtered_df[
            (filtered_df['Date Bid Submitted'] >= f'01/01/{fiscal_year}') &
            (filtered_df['Date Bid Submitted'] < f'12/31/{fiscal_year + 1}')
        ]
        # Filter the winning entries
        win_df = filtered_df[(filtered_df['Award?'] == 'YES')]
        # Filter the losing entries
        lose_df = filtered_df[(filtered_df['Award?'] == 'NO')]

        #Calculate Metrics/Values
        total_bids = len(filtered_df['Date Bid Submitted'])
        total_wins = len(win_df['Award?'])
        total_win_val = round(win_df['Total Value'].sum())
        total_win_val = f"${total_win_val:,.2f}"
        total_lose_val = lose_df['Total Value'].sum()
        Pwin = round((total_wins/total_bids)*100,1)

        #Show latest update date
        st.subheader(":blue[Data Last Updated On: 12/06/2024]")
        
        #Display top metrics
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader("Total Bids")
                st.metric("Total Bids", total_bids, label_visibility="hidden")
        with col2:
            with st.container(border=True):
                st.subheader("Total Awards")
                st.metric("Total Awards", total_wins, label_visibility="hidden")
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader("Total Awarded Value")
                st.metric("Total Awarded Value", total_win_val, label_visibility="hidden")
        with col2:
            with st.container(border=True):
                st.subheader("Win %")
                st.metric("Win %", Pwin, label_visibility="hidden")

        #Display large plots
        plot_agency_counts(filtered_df)
        plot_bids_time(filtered_df)
        plot_brand_pie(filtered_df)

        # Footer
        st.divider()
        st.image(BANNER_PATH,width=300)
        st.write("This is a product of Strategy Ace LLC")
        st.write("version: BETAv0.1")
        st.write(url)

if __name__ == "__main__":
    main()
