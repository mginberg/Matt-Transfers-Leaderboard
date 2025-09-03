import streamlit as st
import pandas as pd

# Google Sheet CSV link (live sync)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ydOa1IBcWFTqxX4Ocm2jqtI4DkgVFkueTPy7n8VIFzY/export?format=csv"
data = pd.read_csv(SHEET_URL)

# Sort leaderboard
data = data.sort_values("Deals", ascending=False).reset_index(drop=True)

# Theme (matches Spin-the-Wheel)
st.set_page_config(page_title="Spin the Wheel Leaderboard", page_icon="🏆", layout="centered")
st.markdown("<h1 style='text-align:center;'>🏆 Monthly Deal Leaderboard</h1>", unsafe_allow_html=True)

# Leaderboard display
for i, row in data.iterrows():
    rank = i + 1
    name = row["Agent"]
    deals = row["Deals"]
    slack_url = row["Slack URL"] if "Slack URL" in row and pd.notna(row["Slack URL"]) else ""

    # Assign medals
    if rank == 1:
        medal = "🥇"
    elif rank == 2:
        medal = "🥈"
    elif rank == 3:
        medal = "🥉"
    else:
        medal = f"{rank}."

    # Layout: profile image + details
    cols = st.columns([1,5])
    with cols[0]:
        if slack_url:
            st.image(slack_url, width=60)
    with cols[1]:
        st.markdown(f"### {medal} {name} — **{deals} deals**")
        st.progress(deals / data['Deals'].max())
