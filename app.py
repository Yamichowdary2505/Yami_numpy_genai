import streamlit as st
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

st.set_page_config(page_title="California Housing Model", page_icon="🏠", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        .stApp { background-color: #f9f9f9; }
        .metric-card {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            margin: 5px;
        }
        .metric-value { font-size: 1.8rem; font-weight: 600; color: #2c3e50; }
        .metric-label { font-size: 0.85rem; color: #7f8c8d; margin-top: 5px; }
        .section-header {
            font-size: 1.1rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
            padding-bottom: 6px;
            border-bottom: 1px solid #e0e0e0;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏠 California Housing Model")
st.caption("Model: Gradient Boosting  |  Dataset: California Housing  |  Split: 80 / 20")
st.divider()

@st.cache_data
def train_and_evaluate():
    data = fetch_california_housing()
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)

    model = GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        min_samples_split=15,
        min_samples_leaf=7,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_train_pred = model.predict(X_train)
    y_test_pred  = model.predict(X_test)

    return {
        "total_samples" : X.shape[0],
        "train_samples" : X_train.shape[0],
        "test_samples"  : X_test.shape[0],
        "features"      : X.shape[1],
        "train_r2"      : r2_score(y_train, y_train_pred),
        "test_r2"       : r2_score(y_test, y_test_pred),
        "train_mse"     : mean_squared_error(y_train, y_train_pred),
        "test_mse"      : mean_squared_error(y_test, y_test_pred),
        "test_rmse"     : np.sqrt(mean_squared_error(y_test, y_test_pred)),
        "test_mae"      : mean_absolute_error(y_test, y_test_pred),
    }

with st.spinner("Training model... please wait."):
    res = train_and_evaluate()

st.markdown('<div class="section-header">📦 Dataset Info</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{res["total_samples"]:,}</div><div class="metric-label">Total Samples</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{res["features"]}</div><div class="metric-label">Features</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{res["train_samples"]:,}</div><div class="metric-label">Train (80%)</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{res["test_samples"]:,}</div><div class="metric-label">Test (20%)</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">📈 R² Score</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{res["train_r2"]:.4f}</div><div class="metric-label">Train R²</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{res["test_r2"]:.4f}</div><div class="metric-label">Test R²</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">📉 Error Metrics</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{res["train_mse"]:.4f}</div><div class="metric-label">Train MSE</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{res["test_mse"]:.4f}</div><div class="metric-label">Test MSE</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{res["test_rmse"]:.4f}</div><div class="metric-label">RMSE</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{res["test_mae"]:.4f}</div><div class="metric-label">MAE</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">🔍 Overfitting Check</div>', unsafe_allow_html=True)
gap = res["train_r2"] - res["test_r2"]
if gap < 0.05:
    status = "✅ No Overfitting"
    color  = "#27ae60"
elif gap < 0.10:
    status = "⚠️ Slight Overfitting"
    color  = "#e67e22"
else:
    status = "❌ Overfitting Detected"
    color  = "#e74c3c"

st.markdown(f"""
    <div class="metric-card">
        <div style="font-size:1.3rem; font-weight:600; color:{color};">{status}</div>
        <div style="font-size:0.95rem; color:#555; margin-top:8px;">Train/Test R² Gap: <b>{gap:.4f}</b></div>
        <div style="font-size:0.82rem; color:#999; margin-top:4px;">Gap below 0.05 = Healthy Model</div>
    </div>
""", unsafe_allow_html=True)

st.divider()
st.caption(f"Test R²: {res['test_r2']:.4f}  |  Test MSE: {res['test_mse']:.4f}  |  RMSE: {res['test_rmse']:.4f}")