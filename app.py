import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Recruitment & HR Analytics Portal", layout="wide")
st.title("📊 Recruitment & HR Analytics Portal")
st.markdown("### Analyze hiring trends across major tech companies")

# ------------------------------
# LOAD DATA
# ------------------------------
# ------------------------------
# LOAD DATA
# ------------------------------
df = pd.read_csv("CSV_files.csv")

# ------------------------------
# DATA PREVIEW TABLE (ADD THIS PART)
# ------------------------------
st.subheader("📄 Recruitment Data Overview")

st.dataframe(
    df.sort_values(by="Hires", ascending=False).head(10),
    use_container_width=True
)

st.caption("Showing Top 10 Records by Hiring Volume")

# ------------------------------
# SIDEBAR FILTERS
# ------------------------------
st.sidebar.header("🔎 Filters")

selected_company = st.sidebar.multiselect(
    "Select Company",
    options=df["Company"].unique(),
    default=df["Company"].unique()
)

selected_role = st.sidebar.multiselect(
    "Select Role",
    options=df["Role"].unique(),
    default=df["Role"].unique()
)

filtered_df = df[
    (df["Company"].isin(selected_company)) &
    (df["Role"].isin(selected_role))
]

# ------------------------------
# KPI SECTION
# ------------------------------
total_hires = filtered_df["Hires"].sum()
total_companies = filtered_df["Company"].nunique()
total_roles = filtered_df["Role"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("👥 Total Hires", total_hires)
col2.metric("🏢 Companies", total_companies)
col3.metric("💼 Roles", total_roles)

st.divider()

# ------------------------------
# TOTAL HIRING BY COMPANY
# ------------------------------
st.subheader("🏢 Total Hiring by Company")

company_total = filtered_df.groupby("Company")["Hires"].sum().reset_index()
st.dataframe(company_total, use_container_width=True)

# ------------------------------
# GROUPED BAR CHART
# ------------------------------
st.subheader("📈 Hiring Trends (Quarter-wise)")

quarter_data = filtered_df.groupby(["Company", "Quarter"])["Hires"].sum().reset_index()
pivot_data = quarter_data.pivot(index="Company", columns="Quarter", values="Hires")

fig, ax = plt.subplots()
pivot_data.plot(kind="bar", ax=ax)
plt.title("Hiring Trends by Company")
plt.ylabel("Number of Hires")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

st.divider()

# ------------------------------
# GROWTH ANALYSIS
# ------------------------------
st.subheader("🚀 Recruitment Growth Analysis")

growth_data = filtered_df.groupby(["Company", "Quarter"])["Hires"].sum().unstack()

if "Q1" in growth_data.columns and "Q2" in growth_data.columns:
    growth_data["Growth"] = growth_data["Q2"] - growth_data["Q1"]
    growth_data["Growth %"] = ((growth_data["Growth"] / growth_data["Q1"]) * 100).round(2)

    st.dataframe(growth_data, use_container_width=True)

    highest_growth_company = growth_data["Growth"].idxmax()
    highest_growth_value = growth_data["Growth"].max()
    highest_growth_percent = growth_data["Growth %"].max()

    st.success(f"🏆 Highest Recruitment Growth: {highest_growth_company}")
    st.info(f"📈 Growth: {highest_growth_value} hires ({highest_growth_percent}%)")

else:
    st.warning("Need at least Q1 and Q2 data to calculate growth.")