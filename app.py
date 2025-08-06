import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="Advanced EDA Tool", page_icon="📊", layout="wide")
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_style("whitegrid")

# Title
st.title("📊 Advanced EDA Analyzer")
st.write("Upload a CSV file to explore your dataset with detailed insights.")

# File Uploader
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"❌ Error reading CSV: {e}")
        st.stop()

    # Dataset Overview
    st.header("1️⃣ Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Duplicates", df.duplicated().sum())

    st.write("**Columns:**", ", ".join(df.columns))

    # Missing Values
    st.header("2️⃣ Missing Values")
    missing = df.isnull().sum()
    missing_df = pd.DataFrame({
        "Missing Count": missing,
        "Missing %": (missing / len(df) * 100).round(2)
    })
    missing_df = missing_df[missing_df["Missing Count"] > 0]
    if missing_df.empty:
        st.success("✅ No missing values found.")
    else:
        st.dataframe(missing_df)

    # Data Type Issues
    st.header("3️⃣ Data Type Suggestions")
    type_suggestions = {}
    for col in df.columns:
        if df[col].dtype == object:
            try:
                pd.to_numeric(df[col])
                type_suggestions[col] = "🔄 Convert to Numeric"
            except:
                try:
                    pd.to_datetime(df[col])
                    type_suggestions[col] = "📅 Convert to Date"
                except:
                    type_suggestions[col] = "Keep as Text"
    st.write(pd.DataFrame.from_dict(type_suggestions, orient='index', columns=["Suggested Type"]))

    # Inconsistent Categories
    st.header("4️⃣ Inconsistent Categories")
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    inconsistent_report = {}
    for col in cat_cols:
        cleaned = df[col].astype(str).str.strip().str.lower()
        unique_vals = cleaned.unique()
        if len(unique_vals) != df[col].nunique():
            inconsistent_report[col] = {
                "Original Unique Count": df[col].nunique(),
                "After Cleaning": len(unique_vals),
                "Possible Fix": "Trim spaces & standardize case"
            }
    if inconsistent_report:
        st.write(pd.DataFrame(inconsistent_report).T)
    else:
        st.success("✅ No inconsistent categories detected.")

    # Column Types
    st.header("5️⃣ Column Type Separation")
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    st.write("**Numeric Columns:**", num_cols)
    st.write("**Categorical Columns:**", cat_cols.tolist())

    # Numerical Analysis
    if num_cols:
        st.header("6️⃣ Numerical Columns Analysis")
        st.subheader("📈 Summary Statistics")
        st.dataframe(df[num_cols].describe().T)

        for col in num_cols:
            st.subheader(f"Distribution of **{col}**")
            fig, ax = plt.subplots(1, 2, figsize=(12, 4))
            sns.histplot(df[col], kde=True, ax=ax[0], color="#48cae4")
            ax[0].set_title(f"Histogram of {col}")
            sns.boxplot(x=df[col], ax=ax[1], color="#ff6b6b")
            ax[1].set_title(f"Boxplot of {col}")
            st.pyplot(fig)

        if len(num_cols) > 1:
            st.subheader("🔗 Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

    # Categorical Analysis
    if cat_cols.any():
        st.header("7️⃣ Categorical Columns Analysis")
        for col in cat_cols:
            st.subheader(f"Count Plot of **{col}**")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.countplot(y=df[col], order=df[col].value_counts().index, palette="viridis")
            ax.set_title(f"Frequency of {col}")
            st.pyplot(fig)

    # Dataset Preview
    st.header("8️⃣ Dataset Preview")
    st.dataframe(df.head())

else:
    st.warning("📂 Please upload a CSV file to start the analysis.")
