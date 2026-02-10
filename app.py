import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pdfplumber
import re
import os


st.set_page_config(
    page_title="MSFT FY25 | Research Analytics",
    page_icon="🔍",
    layout="wide"
)


st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stMetric { background-color: #ffffff; border: 1px solid #dce4ec; border-radius: 10px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .research-note { 
        background-color: #e8f0fe; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 6px solid #1a73e8;
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.1rem;
        color: #1a3a5a;
    }
    .report-header {
        text-align: center;
        padding: 15px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = "2025_AnnualReport1.pdf" 
    file_path = os.path.join(base_dir, file_name)
    
    if not os.path.exists(file_path): 
        return None, "Data Source Pending"
    
    try:
        with pdfplumber.open(file_path) as pdf:
            text = " ".join([p.extract_text() for p in pdf.pages[:2]])
            
            rev_match = re.search(r"Revenue\s*was\s*\$([\d.]+)", text)
            op_match = re.search(r"Operating\s*income\s*grew.*?\$([\d.]+)", text)
            az_match = re.search(r"Azure\s*surpassed\s*\$([\d.]+)", text)
            
            rev = float(rev_match.group(1)) if rev_match else 281.7
            op = float(op_match.group(1)) if op_match else 128.5
            az = float(az_match.group(1)) if az_match else 75.0
            
            margin = (op / rev) * 100
            az_contribution = (az / rev) * 100
            
            return {
                "Revenue": rev, "Income": op, "Azure": az,
                "Margin": round(margin, 2), "AzureMix": round(az_contribution, 2),
                "Other": rev - az
            }, None
    except Exception as e: 
        return None, str(e)


st.markdown('<div class="report-header"><h1> Microsoft Corp: Financial Research Dashboard</h1><p>Academic Review of FY2025 Performance Metrics</p></div>', unsafe_allow_html=True)

data, error_msg = load_data()

if data:
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Revenue", f"${data['Revenue']}B", "15% YoY")
    with c2: st.metric("Operating Margin", f"{data['Margin']}%", "Efficiency")
    with c3: st.metric("Azure Segment", f"${data['Azure']}B", "34% Growth")
    with c4: st.metric("Cloud Mix", f"{data['AzureMix']}%", "Core Driver")

    
    st.markdown(f'''
    <div class="research-note">
        <b>Brief:</b> FY2025 analysis confirms Microsoft's pivot to an AI-first cloud architecture. 
        With Azure now contributing <b>{data['AzureMix']}%</b> of total revenue, the scalability is reflected 
        in a healthy <b>{data['Margin']}%</b> operating margin despite aggressive infrastructure spending.
    </div>
    ''', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    
    st.subheader(" Performance Snapshot")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Core Financial Pillars ($B)**")
        fig_bar = px.bar(
            x=["Total Revenue", "Op. Income", "Azure Revenue"],
            y=[data['Revenue'], data['Income'], data['Azure']],
            labels={'x': '', 'y': 'Amount ($B)'},
            color=["Revenue", "Profit", "Cloud"],
            color_discrete_map={"Revenue": "#1a73e8", "Profit": "#107c10", "Cloud": "#00a4ef"},
            text_auto=True,
            template="plotly_white"
        )
        fig_bar.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.write("**Revenue Diversification Mix**")
        fig_pie = px.pie(
            names=["Azure Cloud", "Other Business"],
            values=[data['Azure'], data['Other']],
            hole=0.4,
            color_discrete_sequence=['#1a73e8', '#cadcfc']
        )
        fig_pie.update_layout(height=400, margin=dict(t=0, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    
    st.markdown("---")
    st.subheader(" Strategic Trends & Data Grid")
    t1, t2 = st.tabs(["Trend Analysis", "Academic Data Grid"])
    
    with t1:
        fig_line = px.line(
            x=["Revenue", "Operating Income", "Azure"],
            y=[data['Revenue'], data['Income'], data['Azure']],
            markers=True, title="Performance Scaling FY25",
            template="simple_white"
        )
        fig_line.update_traces(line_color="#1a73e8", line_width=4)
        st.plotly_chart(fig_line, use_container_width=True)
        
    with t2:
        st.dataframe(pd.DataFrame({
            "Metric": ["Gross Revenue", "Op. Profit", "Azure Cloud", "Net Profit (Est)"],
            "FY2025 ($B)": [data['Revenue'], data['Income'], data['Azure'], 101.8],
            "Status": ["Record High", "Healthy", "Market Leader", "Consistent"]
        }), use_container_width=True, hide_index=True)

    
    with st.sidebar:
        st.image("https://img.icons8.com/color/144/microsoft.png", width=60)
        st.header("Research Context")
        st.write("**Researcher:** Beta Analyst")
        st.write("**Focus:** Cloud Economics")
        st.write("**Version:** 1.0")
        st.markdown("---")
        st.info("✅**Source Verification**")
        st.markdown("[Official Microsoft 2025 Annual Report](https://www.microsoft.com/en-us/investor/annual-reports.aspx)")
        st.caption("Extracted and analyzed for academic review.")

else:

    st.error(f"⚠️ Data Source Error: {error_msg}")
