import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Data Visualizer", page_icon="📊", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #f5f7fa; }
        .stButton>button {
            background-color: #4F8BF9;
            color: white;
            border-radius: 10px;
            font-size: 16px;
            padding: 0.5em 2em;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #2f6de1;
            color: white;
        }
        .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Data Visualizer")
st.caption("Upload a CSV file, select columns and graph type, then generate your chart.")
st.divider()

uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
    df = None
    for enc in encodings:
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding=enc)
            if len(df) > 5000:
                df = df.sample(n=5000, random_state=42)
                st.warning("⚡ Large dataset detected! Showing a random sample of 5,000 rows for faster performance.")
            break
        except Exception:
            continue

    if df is None:
        st.error("⚠️ Could not read the file. Please make sure it is a valid CSV.")
    else:
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown(f"**Rows:** {df.shape[0]} &nbsp;&nbsp; **Columns:** {df.shape[1]}")
        st.divider()

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        all_cols = df.columns.tolist()

        if len(numeric_cols) == 0:
            st.error("⚠️ No numeric columns found in this dataset. Please upload a CSV with numeric data.")
        else:
            col1, col2, col3 = st.columns(3)

            with col1:
                graph_type = st.selectbox("📈 Select Graph Type", [
                    "Bar Chart",
                    "Line Chart",
                    "Scatter Plot",
                    "Histogram",
                    "Pie Chart",
                    "Area Chart",
                    "Box Plot"
                ])

            with col2:
                x_axis = st.selectbox("🔵 X-Axis", all_cols)

            with col3:
                y_axis = st.selectbox("🔴 Y-Axis", numeric_cols)

            color = st.color_picker("🎨 Pick a Chart Color", "#4F8BF9")

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🚀 Generate Graph"):
                st.divider()
                fig, ax = plt.subplots(figsize=(12, 5))
                fig.patch.set_facecolor("#f5f7fa")
                ax.set_facecolor("#ffffff")

                try:
                    if graph_type == "Bar Chart":
                        data = df.groupby(x_axis)[y_axis].mean()
                        ax.bar(data.index.astype(str), data.values, color=color, edgecolor="white")
                        ax.set_xlabel(x_axis)
                        ax.set_ylabel(y_axis)
                        ax.set_title(f"Bar Chart: {y_axis} by {x_axis}")
                        plt.xticks(rotation=45, ha="right")

                    elif graph_type == "Line Chart":
                        ax.plot(df[x_axis].astype(str), df[y_axis], color=color, linewidth=2, marker="o", markersize=4)
                        ax.set_xlabel(x_axis)
                        ax.set_ylabel(y_axis)
                        ax.set_title(f"Line Chart: {y_axis} over {x_axis}")
                        plt.xticks(rotation=45, ha="right")

                    elif graph_type == "Scatter Plot":
                        ax.scatter(df[x_axis], df[y_axis], color=color, alpha=0.6, edgecolors="white", linewidth=0.5)
                        ax.set_xlabel(x_axis)
                        ax.set_ylabel(y_axis)
                        ax.set_title(f"Scatter Plot: {x_axis} vs {y_axis}")
                        m, b = np.polyfit(pd.to_numeric(df[x_axis], errors="coerce").fillna(0), df[y_axis], 1)
                        ax.plot(df[x_axis], m * pd.to_numeric(df[x_axis], errors="coerce").fillna(0) + b, color="red", linewidth=1.5, linestyle="--", label="Trend Line")
                        ax.legend()

                    elif graph_type == "Histogram":
                        ax.hist(df[y_axis].dropna(), bins=20, color=color, edgecolor="white")
                        ax.set_xlabel(y_axis)
                        ax.set_ylabel("Frequency")
                        ax.set_title(f"Histogram of {y_axis}")

                    elif graph_type == "Pie Chart":
                        data = df.groupby(x_axis)[y_axis].sum()
                        if len(data) > 10:
                            data = data.nlargest(10)
                        ax.pie(data.values, labels=data.index.astype(str), autopct="%1.1f%%", startangle=140,
                               colors=plt.cm.Set3(np.linspace(0, 1, len(data))))
                        ax.set_title(f"Pie Chart: {y_axis} by {x_axis}")

                    elif graph_type == "Area Chart":
                        ax.fill_between(range(len(df)), df[y_axis], color=color, alpha=0.4)
                        ax.plot(range(len(df)), df[y_axis], color=color, linewidth=2)
                        ax.set_xlabel(x_axis)
                        ax.set_ylabel(y_axis)
                        ax.set_title(f"Area Chart: {y_axis}")

                    elif graph_type == "Box Plot":
                        ax.boxplot(df[y_axis].dropna(), patch_artist=True,
                                   boxprops=dict(facecolor=color, color="gray"),
                                   medianprops=dict(color="red", linewidth=2))
                        ax.set_ylabel(y_axis)
                        ax.set_title(f"Box Plot of {y_axis}")

                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)
                    plt.tight_layout()
                    st.pyplot(fig)
                    st.success("✅ Graph generated successfully!")

                except Exception as e:
                    st.error(f"⚠️ Could not generate graph: {e}. Try selecting different columns.")

            st.divider()
            st.subheader("📋 Column Statistics")
            st.dataframe(df[numeric_cols].describe().round(2), use_container_width=True)

else:
    st.info("👆 Please upload a CSV file to get started.")
    st.markdown("""
        ### 📌 Supported Graph Types:
        - 📊 Bar Chart
        - 📈 Line Chart
        - 🔵 Scatter Plot
        - 📉 Histogram
        - 🥧 Pie Chart
        - 🌊 Area Chart
        - 📦 Box Plot
    """)
