import streamlit as st
import matplotlib.pyplot as plt
from main import startAnalysis, download_newData
from display import plot_price_history_streamlit, plot_drawdown_streamlit
from metrics import Drawdown_Series
import pandas as pd

st.set_page_config(
    page_title="Stock analyzer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)



def page1():
    st.title("Data & Parameters")
    stock_name= st.text_input(
        "Introduce the name of the stocks:👇"
        )
    stock_names = stock_name.split(",")
    if st.button("Get info", type="primary"):
        results = startAnalysis(stock_names)
        metrics_only = [{k: v for k, v in r.items() if k != "df"} for r in results]
        df_metrics = pd.DataFrame(metrics_only)
        csv = df_metrics.to_csv(index=False)
        for i in results: 
            name = i["Name"]
            total_return = i["Total return"]
            annualize_volatility = i["Annualize volatility"]
            max_drawdown = i["Max Drawdown"]
            simpligy_share_ratio = i["Simplify Sharpe Ratio"]

            col1, col2, col3 = st.columns(3) 

            with col1: 
                st.markdown("NAME")
                st.metric(
                    label = "",
                    value = name.upper(),
                    border=True
                )
            with col2: 
                st.markdown("Total Return")
                st.metric(
                    label="",
                    value=f"{total_return:.2f}",
                    border=True
                )
                st.caption("Higher is better")

                st.markdown("Annualize Volatility")
                st.metric(
                    label="",
                    value=f"{annualize_volatility:.2f}",
                    border=True
                )
                st.caption("lower is better")
            
            with col3: 
                st.markdown("Max Drawdown")
                st.metric(
                    label="",
                    value=f"{max_drawdown:.2f}",
                    border=True
                )
                st.caption("lower is better")

                st.markdown("Simplify Sharpe Ratio")
                st.metric(
                    label="",
                    value=f"{simpligy_share_ratio:.2f}",
                    border=True
                )
                st.caption("higher is better")
            # En app.py — dentro del bucle for ticker_data in results
            fig_price = plot_price_history_streamlit( i["df"], i["Name"])
            st.plotly_chart(fig_price, use_container_width=True)

            drawdown_series = Drawdown_Series(i["df"])
            fig_drawdown = plot_drawdown_streamlit(drawdown_series, i["Name"])
            st.plotly_chart(fig_drawdown, use_container_width=True)

        st.download_button(
        label="Download CSV",
        data=csv,
        file_name="Data_Tickers.csv",
        mime="text/csv",
        icon=":material/download:",
        )



def page2():
    st.title("Predictions/Strategy")


st.title("STOCK ANALYZER")    

pg = st.navigation(
        {"D&A":
            [
                st.Page(page1, title="Data & Parameters", icon="🏦"),
            ], 
        "AI":
            [
                st.Page(page2, title = "Artificial intelligence - Predictions", icon = "🤖"),
            ]
        }
    )
pg.run()