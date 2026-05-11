import streamlit as st
import pandas as pd
from openai import OpenAI

# OpenAI client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# Page title
st.title("AI Prototype: Identity Technical Debt Analyzer")

st.write("""
Upload identity access data to identify:
- dormant privileged access
- missing ownership
- excessive privilege
- identity governance debt
""")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Identity CSV",
    type=["csv"]
)

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Identity Data")
    st.dataframe(df)

    findings = []

    # Risk scoring logic
    for index, row in df.iterrows():

        risk_score = 0
        issues = []

        # High privilege
        if row["access_level"] == "high":
            risk_score += 40
            issues.append("High privilege access")

        # Dormant access
        if row["last_login_days"] > 90:
            risk_score += 40
            issues.append("Dormant access")

        # Missing owner
        if pd.isna(row["owner"]):
            risk_score += 20
            issues.append("Missing ownership")

        # Capture risky identities
        if risk_score >= 60:

            findings.append({
                "user": row["user"],
                "risk_score": risk_score,
                "issues": ", ".join(issues)
            })

    # Findings dataframe
    risk_df = pd.DataFrame(findings)

    st.subheader("Identity Technical Debt Findings")

    if not risk_df.empty:

        st.dataframe(risk_df)

        # Chart
        st.bar_chart(
            risk_df.set_index("user")["risk_score"]
        )

        # Total debt score
        total_debt = risk_df["risk_score"].sum()

        st.metric(
            "Identity Technical Debt Score",
            total_debt
        )

        # GPT Analysis
        st.subheader("AI Governance Insights")

        risk_summary = risk_df.to_string(index=False)

        prompt = f"""
        Analyze the following identity governance findings.

        Identify:
        - identity technical debt patterns
        - governance weaknesses
        - excessive privilege risks
        - lifecycle management gaps
        - remediation priorities

        Provide concise executive-level insights.

        Findings:
        {risk_summary}
        """

        with st.spinner("Generating AI insights..."):

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior enterprise IAM governance expert."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )

            ai_output = response.choices[0].message.content

            st.write(ai_output)

    else:

        st.success("No major identity governance debt detected.")
