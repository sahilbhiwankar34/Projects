import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# PAGE TITLE
# ------------------------------
st.set_page_config(page_title="Recruitment & HR Analytics Portal", layout="wide")
st.title("📊 Recruitment & HR Analytics Portal")

# ------------------------------
# LOAD DATA
# ------------------------------
df = pd.read_csv("CSV_files.csv")

st.subheader("📁 Raw Dataset")
st.dataframe(df)

# ------------------------------
# GROUP BY COMPANY
# ------------------------------
st.subheader("🏢 Total Hiring by Company")

company_total = df.groupby("Company")["Hires"].sum().reset_index()
st.dataframe(company_total)

# ------------------------------
# GROUP BY COMPANY & ROLE
# ------------------------------
st.subheader("👨‍💻 Hiring by Company & Role")

company_role = df.groupby(["Company", "Role"])["Hires"].sum().reset_index()
st.dataframe(company_role)

# ------------------------------
# GROUPED BAR CHART (Quarter-wise Hiring Trends)
# ------------------------------
st.subheader("📈 Hiring Trends (Quarter-wise)")

quarter_data = df.groupby(["Company", "Quarter"])["Hires"].sum().reset_index()

pivot_data = quarter_data.pivot(index="Company", columns="Quarter", values="Hires")

fig, ax = plt.subplots()
pivot_data.plot(kind="bar", ax=ax)

plt.title("Hiring Trends by Company (Quarter-wise)")
plt.ylabel("Number of Hires")
plt.xticks(rotation=45)

st.pyplot(fig)

# ------------------------------
# RECRUITMENT GROWTH CALCULATION
# ------------------------------
st.subheader("🚀 Recruitment Growth Analysis")

growth_data = df.groupby(["Company", "Quarter"])["Hires"].sum().unstack()

# Ensure Q1 and Q2 exist
if "Q1" in growth_data.columns and "Q2" in growth_data.columns:
    growth_data["Growth"] = growth_data["Q2"] - growth_data["Q1"]
    st.dataframe(growth_data)

    highest_growth_company = growth_data["Growth"].idxmax()
    highest_growth_value = growth_data["Growth"].max()

    st.success(f"🏆 Company with Highest Recruitment Growth: {highest_growth_company}")
    st.write(f"Growth Value: {highest_growth_value} hires")
else:
    st.warning("Need at least Q1 and Q2 data to calculate growth.")