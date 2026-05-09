import streamlit as st
from main import startAnalysis
from display import plot_price_history_streamlit, plot_drawdown_streamlit, plot_signals_streamlit, plot_backtest_streamlit
from metrics import Drawdown_Series
from model import create_features, create_target, train_model, backtesting
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
    select_period =  st.selectbox("Select period:", ["1y", "2y", "5y", "10y"])
    if st.button("Get info", type="primary"):
        results = startAnalysis(stock_names,select_period)
        if stock_name == "":
            st.warning('Necessary to introduce at least one stock to analyze')
        elif results == []: 
            st.warning(f'stock not found for "{stock_names[0].upper()}". Check if you write it correctly', icon="⚠️") 
        else:
            metrics_only = [{k: v for k, v in r.items() if k != "df"} for r in results]
            df_metrics = pd.DataFrame(metrics_only)
            csv = df_metrics.to_csv(index=False)
            successful = [r["Name"] for r in results]
            failed = [s.strip().upper() for s in stock_names if s.strip().upper() not in successful]
            for ticker in failed:
                st.warning(f"Ticker '{ticker}' not found. Check if you wrote it correctly.", icon="⚠️")
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
    st.title("Predictions sell/buy")
    stock_name= st.text_input(
        "Introduce the name of the stocks that you want to predict:👇"
        )
    stock_names = stock_name.split(",")
    select_period =  st.selectbox("Select period:", ["1y", "2y", "5y", "10y"])
    if st.button("Get Predictions", type="primary"):
        results = startAnalysis(stock_names,select_period)
        if stock_name == "":
            st.warning('Necessary to introduce at least one stock to analyze')
        elif results == []: 
            st.warning(f'stock not found for "{stock_names[0].upper()}". Check if you write it correctly', icon="⚠️") 
        else:
            successful = [r["Name"] for r in results]
            failed = [s.strip().upper() for s in stock_names if s.strip().upper() not in successful]
            for ticker in failed:
                st.warning(f"Ticker '{ticker}' not found. Check if you wrote it correctly.", icon="⚠️")
        for i in results: 
            df = create_target(i["df"])
            df = create_features(i["df"])
            model, signals, report = train_model(df)
            df["Signal"] = signals
            df = backtesting(df)          
            fig_signals = plot_signals_streamlit(df, i["Name"])
            st.plotly_chart(fig_signals, use_container_width=True)
            fig_backtesting = plot_backtest_streamlit(df, i["Name"])
            st.plotly_chart(fig_backtesting, use_container_width=True)



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