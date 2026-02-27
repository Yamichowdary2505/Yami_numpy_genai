import streamlit as st
import requests

st.set_page_config(
    page_title="Currency Converter",
    page_icon="💱",
    layout="centered"
)

st.markdown("""
    <style>
        .main { background-color: #f0f4f8; }
        .stButton>button {
            background-color: #4F8BF9;
            color: white;
            border-radius: 10px;
            padding: 0.5em 2em;
            font-size: 16px;
            width: 100%;
        }
        .result-box {
            background-color: #e8f0fe;
            border-left: 5px solid #4F8BF9;
            padding: 20px;
            border-radius: 10px;
            font-size: 22px;
            text-align: center;
            margin-top: 20px;
        }
        .rate-box {
            background-color: #f1f8e9;
            border-left: 5px solid #66bb6a;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            color: #444;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("💱 Currency Converter")
st.caption("Real-time exchange rates powered by the Open Exchange Rates API")
st.divider()

CURRENCIES = [
    "USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD", "CHF",
    "CNY", "SGD", "AED", "SAR", "NZD", "HKD", "SEK", "NOK",
    "MXN", "BRL", "ZAR", "KRW"
]

if "from_currency" not in st.session_state:
    st.session_state.from_currency = "USD"
if "to_currency" not in st.session_state:
    st.session_state.to_currency = "INR"

@st.cache_data(ttl=3600)
def get_exchange_rates(base_currency):
    try:
        url = f"https://open.er-api.com/v6/latest/{base_currency}"
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("result") == "success":
            return data["rates"], data.get("time_last_update_utc", "N/A")
        else:
            return None, None
    except Exception:
        return None, None

def swap_currencies():
    st.session_state.from_currency, st.session_state.to_currency = (
        st.session_state.to_currency,
        st.session_state.from_currency,
    )

col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    from_currency = st.selectbox(
        "🏦 From Currency",
        CURRENCIES,
        index=CURRENCIES.index(st.session_state.from_currency),
        key="from_select"
    )
    st.session_state.from_currency = from_currency

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.button("⇄ Swap", on_click=swap_currencies)

with col3:
    to_currency = st.selectbox(
        "💰 To Currency",
        CURRENCIES,
        index=CURRENCIES.index(st.session_state.to_currency),
        key="to_select"
    )
    st.session_state.to_currency = to_currency

amount = st.number_input(
    f"Enter amount in {st.session_state.from_currency}",
    min_value=0.01,
    value=1.00,
    step=1.0,
    format="%.2f"
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔄 Convert"):
    with st.spinner("Fetching latest exchange rates..."):
        rates, last_updated = get_exchange_rates(st.session_state.from_currency)

    if rates:
        if st.session_state.to_currency in rates:
            rate = rates[st.session_state.to_currency]
            converted = amount * rate

            st.markdown(f"""
                <div class="result-box">
                    <b>{amount:,.2f} {st.session_state.from_currency}</b> = 
                    <span style="color:#4F8BF9; font-size:28px;"><b>{converted:,.4f} {st.session_state.to_currency}</b></span>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="rate-box">
                    📌 <b>1 {st.session_state.from_currency}</b> = <b>{rate:.6f} {st.session_state.to_currency}</b> &nbsp;|&nbsp;
                    🕒 Last updated: {last_updated}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Currency '{st.session_state.to_currency}' not found in the rates.")
    else:
        st.error("⚠️ Could not fetch exchange rates. Please check your internet connection.")

st.divider()

with st.expander("📊 Compare with Multiple Currencies"):
    st.write(f"**Conversion of {amount:,.2f} {st.session_state.from_currency} to multiple currencies:**")
    rates_data, _ = get_exchange_rates(st.session_state.from_currency)
    if rates_data:
        compare_currencies = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD", "CHF", "CNY", "SGD"]
        table_data = {
            "Currency": compare_currencies,
            "Exchange Rate": [f"{rates_data.get(c, 'N/A'):.4f}" for c in compare_currencies],
            f"Value ({amount:.2f} {st.session_state.from_currency})": [
                f"{amount * rates_data[c]:,.4f}" if c in rates_data else "N/A"
                for c in compare_currencies
            ]
        }
        st.table(table_data)

st.divider()
st.caption("📡 Data sourced from open.er-api.com · Rates updated hourly · Built with Streamlit 🚀")