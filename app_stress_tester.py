
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="📉 Portfolio Stress Testing App", layout="wide")
st.title("📉 Portfolio Stress Testing App")
st.caption("Upload a portfolio and simulate shocks across various stress scenarios.")

# --- Upload file ---
uploaded_file = st.file_uploader("Upload your portfolio file (Excel)", type=["xlsx"])

if uploaded_file:
    portfolio = pd.read_excel(uploaded_file)
    st.subheader("Portfolio Preview")
    st.dataframe(portfolio.head())

    if not {"Instrument", "Price", "Quantity"}.issubset(portfolio.columns):
        st.error("Your file must contain 'Instrument', 'Price', and 'Quantity' columns.")
    else:
        scenario_type = st.radio("Select Stress Scenario", [
            "Specified Shocks Scenario",
            "Date Range Scenario",
            "Implied Shocks Scenario",
            "Named Scenario"
        ])

        if scenario_type == "Specified Shocks Scenario":
            st.info("You define shock % per instrument. Negative values represent losses.")
            for i in range(len(portfolio)):
                instrument = portfolio.loc[i, "Instrument"]
                shock = st.number_input(f"Shock % for {instrument}", min_value=-1.0, max_value=1.0, value=0.0, step=0.01)
                portfolio.loc[i, "Shock"] = shock

        elif scenario_type == "Implied Shocks Scenario":
            st.info("Apply multiplier to each instrument's implied volatility.")
            if "Volatility" not in portfolio.columns:
                st.error("Your file must include a 'Volatility' column for this scenario.")
            else:
                multiplier = st.slider("Implied Volatility Multiplier", 0.1, 5.0, 2.0, 0.1)
                portfolio["Shock"] = -portfolio["Volatility"] * multiplier

        elif scenario_type == "Date Range Scenario":
            st.warning("This scenario requires historical prices, which would normally be sourced from a database or API.")
            st.stop()

        elif scenario_type == "Named Scenario":
            scenario_options = {
                "Global Financial Crisis 2008": {"AAPL": -0.5, "MSFT": -0.3},
                "US-China Trade War": {"AAPL": -0.15, "MSFT": -0.1},
                "Interest Rates Rise": {"AAPL": -0.2, "MSFT": -0.2},
                "US Downgrade ‘11": {"AAPL": -0.25, "MSFT": -0.15},
                "North Korea Conflict": {"AAPL": -0.35, "MSFT": -0.25},
                "Credit Spreads Widen": {"AAPL": -0.3, "MSFT": -0.2}
            }
            selected_scenario = st.selectbox("Choose Named Scenario", list(scenario_options.keys()))
            shocks = scenario_options[selected_scenario]
            portfolio["Shock"] = portfolio["Instrument"].map(shocks).fillna(0.0)

        # --- Apply Shock and Calculate P&L ---
        portfolio["Shocked Price"] = portfolio["Price"] * (1 + portfolio["Shock"])
        portfolio["P&L"] = (portfolio["Shocked Price"] - portfolio["Price"]) * portfolio["Quantity"]

        st.subheader("Stress Testing Results")
        st.metric("Total Stress P&L", f"${portfolio['P&L'].sum():,.2f}")
        st.dataframe(portfolio[["Instrument", "Price", "Shocked Price", "Shock", "Quantity", "P&L"]])

        fig = px.bar(portfolio, x="Instrument", y="P&L", color="Shock", title="P&L Impact by Instrument")
        st.plotly_chart(fig, use_container_width=True)

        # --- Download Results ---
        def convert_df(df):
            return df.to_excel(index=False, engine='openpyxl')

        st.download_button(
            label="📥 Download Stress Results",
            data=convert_df(portfolio),
            file_name="stress_testing_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Please upload a portfolio Excel file to begin.")
