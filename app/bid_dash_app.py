import streamlit as st
import pandas as pd
from app.plots import plot_agency_counts, plot_bids_time, plot_brand_pie
from app.auth import authenticate

PATH = 'data/sample_data.csv'

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
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
        st.title("Bid Dashboard")
        fiscal_year = 2024
        df = pd.read_csv(PATH)
        df['Date Bid Submitted'] = pd.to_datetime(df['Date Bid Submitted'], format='%m/%d/%Y', errors='coerce')
        filtered_df = df[pd.notnull(df['Date Bid Submitted'])]
        filtered_df = filtered_df[
            (filtered_df['Date Bid Submitted'] >= f'01/01/{fiscal_year}') &
            (filtered_df['Date Bid Submitted'] < f'12/31/{fiscal_year + 1}')
        ]
        total_bids = len(filtered_df)
        st.metric("Total Bids", total_bids)
        plot_agency_counts(filtered_df)
        plot_bids_time(filtered_df)
        plot_brand_pie(filtered_df)

if __name__ == "__main__":
    main()
