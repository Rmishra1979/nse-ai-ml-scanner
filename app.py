
import streamlit as st
from scanner import run_full_scan
from model import train_models, predict_probability
from auth import login_screen

st.set_page_config(page_title="NSE AI ML Scanner", layout="wide")

user = login_screen()

if user:
    st.title("📊 NSE AI ML HA-Reversal Scanner")

    if st.button("Train ML Models"):
        train_models()
        st.success("Models Trained Successfully")

    if st.button("Run AI Scan with Probability"):
        results = run_full_scan()
        if results.empty:
            st.warning("No signals found.")
        else:
            results['Probability'] = results.apply(
                lambda row: predict_probability(row['score']), axis=1
            )
            st.dataframe(results)
