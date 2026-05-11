import streamlit as st
import pandas as pd

st.title("AI Prototype: Identity Technical Debt Analyzer")

uploaded_file = st.file_uploader(
    "Upload Identity CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Identity Data")
    st.dataframe(df)

    findings = []

    for index, row in df.iterrows():

        risk_score = 0
        issues = []

        if row["access_level"] == "high":
            risk_score += 40
            issues.append("High privilege access")

        if row["last_login_days"] > 90:
            risk_score += 40
            issues.append("Dormant access")

        if pd.isna(row["owner"]):
            risk_score += 20
            issues.append("Missing ownership")

        if risk_score >= 60:
            findings.append({
                "user": row["user"],
                "risk_score": risk_score,
                "issues": ", ".join(issues)
            })

    risk_df = pd.DataFrame(findings)

    st.subheader("Identity Technical Debt Findings")
    st.dataframe(risk_df)

    if not risk_df.empty:
        st.bar_chart(
            risk_df.set_index("user")["risk_score"]
        )

        total_debt = risk_df["risk_score"].sum()

        st.metric(
            "Identity Technical Debt Score",
            total_debt
        )
