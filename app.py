"""
PLE Data Analysis Dashboard
Interactive Streamlit Dashboard with Plotly Visualizations
Connects to Google Sheets for live data analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings("ignore")

# Page configuration
st.set_page_config(
    page_title="PLE Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS - Modern Professional Design
st.markdown(
    """
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main background with subtle pattern */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        background-attachment: fixed;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Sidebar with glassmorphism effect */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.06);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    /* Enhanced metric cards with hover effects */
    .stMetric {
        background: rgba(255, 255, 255, 0.95);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }
    
    .stMetric:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
    }
    
    .stMetric label {
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #6b7280;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Headers with modern styling */
    h1 {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1f2937;
        margin-top: 2rem;
        margin-bottom: 1rem;
        letter-spacing: -0.3px;
    }
    
    h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: #374151;
        margin-top: 1.5rem;
    }
    
    /* Modern tabs with animated underline */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: rgba(255, 255, 255, 0.9);
        padding: 6px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #6b7280;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 12px 24px;
        border: none;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Premium button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Modern select boxes */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid #e5e7eb;
        border-radius: 10px;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
    }
    
    .stSelectbox > div > div:focus-within,
    .stMultiSelect > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
    }
    
    /* Stylish multiselect tags */
    .stMultiSelect span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stMultiSelect span[data-baseweb="tag"] svg {
        fill: white !important;
    }
    
    /* Modern radio buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.9);
        padding: 10px;
        border-radius: 10px;
        gap: 8px;
    }
    
    .stRadio label {
        background: white !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        border: 2px solid #e5e7eb !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        cursor: pointer !important;
    }
    
    .stRadio label:hover {
        border-color: #667eea !important;
        background: rgba(102, 126, 234, 0.05) !important;
        transform: scale(1.02);
    }
    
    .stRadio label[data-checked="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Premium dataframe styling */
    .stDataFrame {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    }
    
    [data-testid="stDataFrame"] {
        background: white !important;
    }
    
    [data-testid="stDataFrame"] table {
        background: white !important;
    }
    
    [data-testid="stDataFrame"] thead tr th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        padding: 16px 12px !important;
        border: none !important;
    }
    
    [data-testid="stDataFrame"] tbody tr {
        background: white !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stDataFrame"] tbody tr:nth-child(even) {
        background: #f9fafb !important;
    }
    
    [data-testid="stDataFrame"] tbody tr:hover {
        background: rgba(102, 126, 234, 0.08) !important;
        transform: scale(1.01);
    }
    
    [data-testid="stDataFrame"] td {
        color: #374151 !important;
        padding: 14px 12px !important;
        font-weight: 500 !important;
        border-bottom: 1px solid #f3f4f6 !important;
    }
    
    /* Beautiful success messages */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
    }
    
    /* Dividers with gradient */
    hr {
        margin: 32px 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%);
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Color palette - Modern vibrant colors
COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "success": "#06d6a0",
    "warning": "#ffd93d",
    "danger": "#ef476f",
    "info": "#118ab2",
    "boys": "#4c9aff",
    "girls": "#ff9500",
    "divisions": ["#06d6a0", "#118ab2", "#ffd93d", "#ef476f", "#a29bfe", "#6c5ce7"],
    "gradient1": ["#667eea", "#764ba2"],
    "gradient2": ["#06d6a0", "#118ab2"],
    "chart_colors": ["#667eea", "#06d6a0", "#ffd93d", "#ef476f", "#4c9aff", "#a29bfe"],
}

# Google Sheet configuration
GOOGLE_SHEET_ID = "1X8Iwe1jbmkFZ1SHH6ayHx6YE11hamr6idJ68-L-KJF8"


@st.cache_data
def load_from_google_sheet(sheet_id, sheet_name="Sheet1"):
    """Load data from public Google Sheets"""
    try:
        export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(export_url)
        return df
    except Exception as e:
        st.error(f"Error loading Google Sheet: {e}")
        return None


@st.cache_data
def clean_and_process_data(df):
    """Clean and calculate metrics for PLE data"""
    if df is None:
        return None

    df = df.copy()

    # Remove empty rows
    df = df.dropna(how="all")

    # Reset index to avoid duplicate index issues
    df = df.reset_index(drop=True)

    # Fix duplicate column names by adding suffix
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [
            dup + "_" + str(i) if i != 0 else dup for i in range(sum(cols == dup))
        ]
    df.columns = cols

    # Identify numeric columns
    numeric_patterns = [
        "Div",
        "Division",
        "Boys",
        "Girls",
        "Total",
        "Registered",
        "Pass",
        "Rate",
        "M",
        "F",
    ]
    numeric_cols = [
        col
        for col in df.columns
        if any(pattern in str(col) for pattern in numeric_patterns)
    ]

    # Convert to numeric
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Detect if we have standard PLE structure
    has_divisions = any("Div" in str(col) for col in df.columns)

    if has_divisions:
        # Map column names to standard format
        col_mapping = {}
        for col in df.columns:
            col_str = str(col)
            # Map division columns
            if "Div1" in col_str or "Division 1" in col_str:
                if "_M" in col_str or "Boys" in col_str:
                    col_mapping[col] = "Division 1 - Boys"
                elif "_F" in col_str or "Girls" in col_str:
                    col_mapping[col] = "Division 1 - Girls"
                elif "Total" in col_str:
                    col_mapping[col] = "Division 1 - Total"
            elif "Div2" in col_str or "Division 2" in col_str:
                if "_M" in col_str or "Boys" in col_str:
                    col_mapping[col] = "Division 2 - Boys"
                elif "_F" in col_str or "Girls" in col_str:
                    col_mapping[col] = "Division 2 - Girls"
                elif "Total" in col_str:
                    col_mapping[col] = "Division 2 - Total"
            elif "Div3" in col_str or "Division 3" in col_str:
                if "_M" in col_str or "Boys" in col_str:
                    col_mapping[col] = "Division 3 - Boys"
                elif "_F" in col_str or "Girls" in col_str:
                    col_mapping[col] = "Division 3 - Girls"
                elif "Total" in col_str:
                    col_mapping[col] = "Division 3 - Total"
            elif "Div4" in col_str or "Division 4" in col_str:
                if "_M" in col_str or "Boys" in col_str:
                    col_mapping[col] = "Division 4 - Boys"
                elif "_F" in col_str or "Girls" in col_str:
                    col_mapping[col] = "Division 4 - Girls"
                elif "Total" in col_str:
                    col_mapping[col] = "Division 4 - Total"
            elif "DivU" in col_str or "Division U" in col_str:
                if "_M" in col_str or "Boys" in col_str:
                    col_mapping[col] = "Division U - Boys"
                elif "_F" in col_str or "Girls" in col_str:
                    col_mapping[col] = "Division U - Girls"
                elif "Total" in col_str:
                    col_mapping[col] = "Division U - Total"
            elif "DivX" in col_str or "Division X" in col_str:
                if "_M" in col_str or "Boys" in col_str:
                    col_mapping[col] = "Division X - Boys"
                elif "_F" in col_str or "Girls" in col_str:
                    col_mapping[col] = "Division X - Girls"
                elif "Total" in col_str:
                    col_mapping[col] = "Division X - Total"
            # Map district/area columns
            if "Area" in col_str and "District" not in col_str:
                col_mapping[col] = "District"

        df = df.rename(columns=col_mapping)

        # After renaming, check for duplicate column names again and fix
        if df.columns.duplicated().any():
            cols = pd.Series(df.columns)
            for dup in cols[cols.duplicated()].unique():
                cols[cols[cols == dup].index.values.tolist()] = [
                    dup + "_dup" + str(i) if i != 0 else dup
                    for i in range(sum(cols == dup))
                ]
            df.columns = cols

        # Calculate totals if not present - using .values to avoid index alignment
        if "Registered - Total" not in df.columns:
            if (
                all(f"Division {i} - Total" in df.columns for i in range(1, 5))
                and "Division U - Total" in df.columns
            ):
                total = (
                    df["Division 1 - Total"].fillna(0).values
                    + df["Division 2 - Total"].fillna(0).values
                    + df["Division 3 - Total"].fillna(0).values
                    + df["Division 4 - Total"].fillna(0).values
                    + df["Division U - Total"].fillna(0).values
                )
                if "Division X - Total" in df.columns:
                    total = total + df["Division X - Total"].fillna(0).values
                df["Registered - Total"] = total

        # Calculate boys and girls totals
        if "Registered - Boys" not in df.columns:
            boys_cols = [
                "Division 1 - Boys",
                "Division 2 - Boys",
                "Division 3 - Boys",
                "Division 4 - Boys",
                "Division U - Boys",
                "Division X - Boys",
            ]
            total_boys = np.zeros(len(df))
            for col in boys_cols:
                if col in df.columns:
                    total_boys = total_boys + df[col].fillna(0).values
            df["Registered - Boys"] = total_boys

        if "Registered - Girls" not in df.columns:
            girls_cols = [
                "Division 1 - Girls",
                "Division 2 - Girls",
                "Division 3 - Girls",
                "Division 4 - Girls",
                "Division U - Girls",
                "Division X - Girls",
            ]
            total_girls = np.zeros(len(df))
            for col in girls_cols:
                if col in df.columns:
                    total_girls = total_girls + df[col].fillna(0).values
            df["Registered - Girls"] = total_girls

        # Calculate performance metrics
        pass_cols = [
            "Division 1 - Total",
            "Division 2 - Total",
            "Division 3 - Total",
            "Division 4 - Total",
        ]
        passed = np.zeros(len(df))
        for col in pass_cols:
            if col in df.columns:
                passed = passed + df[col].fillna(0).values
        df["Passed_Total"] = passed

        fail_cols = ["Division U - Total", "Division X - Total"]
        failed = np.zeros(len(df))
        for col in fail_cols:
            if col in df.columns:
                failed = failed + df[col].fillna(0).values
        df["Failed_Total"] = failed

        # Calculate rates (avoid division by zero)
        div1_for_rate = (
            df["Division 1 - Total"].fillna(0).values
            if "Division 1 - Total" in df.columns
            else np.zeros(len(df))
        )
        div2_for_rate = (
            df["Division 2 - Total"].fillna(0).values
            if "Division 2 - Total" in df.columns
            else np.zeros(len(df))
        )
        div3_for_rate = (
            df["Division 3 - Total"].fillna(0).values
            if "Division 3 - Total" in df.columns
            else np.zeros(len(df))
        )

        df["Pass_Rate"] = np.where(
            df["Registered - Total"] > 0,
            (df["Passed_Total"] / df["Registered - Total"] * 100).round(2),
            0,
        )
        df["Excellence_Rate"] = np.where(
            df["Registered - Total"] > 0,
            (div1_for_rate / df["Registered - Total"].values * 100).round(2),
            0,
        )
        df["Strong_Performance_Rate"] = np.where(
            df["Registered - Total"] > 0,
            (
                (div1_for_rate + div2_for_rate + div3_for_rate)
                / df["Registered - Total"].values
                * 100
            ).round(2),
            0,
        )

        # Gender metrics
        boys_pass_cols = [
            "Division 1 - Boys",
            "Division 2 - Boys",
            "Division 3 - Boys",
            "Division 4 - Boys",
        ]
        boys_passed = np.zeros(len(df))
        for col in boys_pass_cols:
            if col in df.columns:
                boys_passed = boys_passed + df[col].fillna(0).values

        girls_pass_cols = [
            "Division 1 - Girls",
            "Division 2 - Girls",
            "Division 3 - Girls",
            "Division 4 - Girls",
        ]
        girls_passed = np.zeros(len(df))
        for col in girls_pass_cols:
            if col in df.columns:
                girls_passed = girls_passed + df[col].fillna(0).values

        df["Boys_Pass_Rate"] = np.where(
            df["Registered - Boys"] > 0,
            (boys_passed / df["Registered - Boys"].values * 100).round(2),
            0,
        )
        df["Girls_Pass_Rate"] = np.where(
            df["Registered - Girls"] > 0,
            (girls_passed / df["Registered - Girls"].values * 100).round(2),
            0,
        )
        df["Gender_Gap"] = (df["Boys_Pass_Rate"] - df["Girls_Pass_Rate"]).round(2)

    return df


def main():
    # Modern Hero Header
    st.markdown(
        """
        <div style='text-align: center; padding: 15px 20px; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    border-radius: 20px; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);'>
            <h1 style='font-size: 3.5em; font-weight: 800; margin: 10px 0; letter-spacing: -1px;'>
                PLE Data Analysis Dashboard
            </h1>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Sidebar with enhanced design
    with st.sidebar:
        st.markdown(
            """
            <div style='text-align: center; padding: 24px; margin-bottom: 24px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 16px; box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);'>
                <h2 style='margin: 0; color: white; font-size: 1.5em; font-weight: 700; letter-spacing: -0.3px;'>
                    Control Panel
                </h2>
                <p style='margin: 8px 0 0 0; color: rgba(255,255,255,0.9); font-size: 0.9em;'>
                    Filter & Analyze Your Data
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Load data
        with st.spinner("Loading data from Google Sheets..."):
            raw_data = load_from_google_sheet(GOOGLE_SHEET_ID, "Sheet1")

            if raw_data is not None:
                data = clean_and_process_data(raw_data)

                if data is not None:
                    # Filters
                    st.subheader("🔍 Filters")

                    # Year filter
                    if "Year" in data.columns:
                        years = ["All"] + sorted(
                            data["Year"].dropna().unique().tolist(), reverse=True
                        )
                        year_options = [y for y in years if y != "All"]
                        default_year = (
                            [2025]
                            if 2025 in year_options
                            else (year_options[:1] if year_options else [])
                        )
                        selected_years = st.multiselect(
                            "Year:",
                            options=year_options,
                            default=default_year,
                            help="Select years to include in analysis",
                        )
                    else:
                        selected_years = None

                    # Gender filter
                    gender_filter = st.radio(
                        "View:",
                        options=["All", "Boys Only", "Girls Only"],
                        horizontal=True,
                    )

                    # Sub Region filter
                    if "Sub Region" in data.columns:
                        sub_regions = ["All"] + sorted(
                            data["Sub Region"].dropna().unique().tolist()
                        )
                        selected_sub_region = st.selectbox(
                            "Sub Region:",
                            options=sub_regions,
                        )
                    else:
                        selected_sub_region = "All"

                    # Zonal Office filter
                    if "Zone" in data.columns:
                        zones = ["All"] + sorted(
                            data["Zone"].dropna().unique().tolist()
                        )
                        selected_zone = st.selectbox(
                            "Zonal Office:",
                            options=zones,
                        )
                    else:
                        selected_zone = "All"

                    # District filter
                    if "District" in data.columns:
                        districts = ["All"] + sorted(
                            data["District"].dropna().unique().tolist()
                        )
                        selected_district = st.selectbox(
                            "District:",
                            options=districts,
                        )
                    else:
                        selected_district = "All"

                    # Grade filter
                    grade_filter = st.multiselect(
                        "Grade/Division:",
                        options=[
                            "Division 1",
                            "Division 2",
                            "Division 3",
                            "Division 4",
                            "Division U",
                            "Division X",
                        ],
                        default=[
                            "Division 1",
                            "Division 2",
                            "Division 3",
                            "Division 4",
                        ],
                        help="Select divisions to include in analysis",
                    )

                    st.markdown("---")

                    # Refresh button
                    if st.button("🔄 Refresh Data", type="primary"):
                        st.cache_data.clear()
                        st.rerun()

                    st.markdown("---")

                    # Data load success message
                    st.markdown(
                        f"""
                        <div style='background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                                    padding: 16px; border-radius: 12px; border-left: 4px solid #10b981;
                                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2); margin: 16px 0;'>
                            <div style='display: flex; align-items: center; gap: 12px;'>
                                <span style='font-size: 1.5em;'>✓</span>
                                <div>
                                    <div style='font-weight: 600; color: #065f46;'>Data Loaded Successfully</div>
                                    <div style='font-size: 0.9em; color: #047857; margin-top: 4px;'>
                                        {len(raw_data):,} records from Google Sheets
                                    </div>
                                </div>
                            </div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    # Store original data for gender calculations
                    original_data = data.copy()

                    # Apply filters
                    if selected_years and "Year" in data.columns:
                        data = data[data["Year"].isin(selected_years)]

                    if selected_sub_region != "All":
                        data = data[data["Sub Region"] == selected_sub_region]

                    if selected_zone != "All":
                        data = data[data["Zone"] == selected_zone]

                    if selected_district != "All":
                        data = data[data["District"] == selected_district]

                    # Modern sidebar metrics with icons
                    st.markdown(
                        "<div style='margin-top: 20px;'></div>", unsafe_allow_html=True
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(
                            f"""
                            <div style='background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%); 
                                        padding: 16px; border-radius: 12px; text-align: center;
                                        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);'>
                                <div style='font-size: 1.8em; margin-bottom: 8px;'>📁</div>
                                <div style='font-size: 0.8em; color: #5b21b6; font-weight: 600; text-transform: uppercase;'>Total</div>
                                <div style='font-size: 1.8em; font-weight: 700; color: #6d28d9; margin-top: 4px;'>{len(original_data):,}</div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.markdown(
                            f"""
                            <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                                        padding: 16px; border-radius: 12px; text-align: center;
                                        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);'>
                                <div style='font-size: 1.8em; margin-bottom: 8px;'>🎯</div>
                                <div style='font-size: 0.8em; color: #1e3a8a; font-weight: 600; text-transform: uppercase;'>Filtered</div>
                                <div style='font-size: 1.8em; font-weight: 700; color: #1e40af; margin-top: 4px;'>{len(data):,}</div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    if len(data) > 0 and "District" in data.columns:
                        st.markdown(
                            f"""
                            <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                                        padding: 16px; border-radius: 12px; text-align: center; margin-top: 12px;
                                        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);'>
                                <div style='font-size: 1.8em; margin-bottom: 8px;'>🏛️</div>
                                <div style='font-size: 0.8em; color: #78350f; font-weight: 600; text-transform: uppercase;'>Districts</div>
                                <div style='font-size: 1.8em; font-weight: 700; color: #92400e; margin-top: 4px;'>{data["District"].nunique()}</div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.error("Failed to process data")
                    data = None
            else:
                st.error("Failed to load data")
                data = None

    # Main content
    if data is not None and not data.empty:
        # Apply gender filter to metrics
        if gender_filter == "Boys Only":
            total_students = data["Registered - Boys"].sum()
            pass_rate_metric = data["Boys_Pass_Rate"].mean()
        elif gender_filter == "Girls Only":
            total_students = data["Registered - Girls"].sum()
            pass_rate_metric = data["Girls_Pass_Rate"].mean()
        else:
            total_students = data["Registered - Total"].sum()
            pass_rate_metric = data["Pass_Rate"].mean()

        # Calculate grade-specific metrics based on filter
        if grade_filter:
            grade_totals = 0
            for grade in grade_filter:
                col_name = f"{grade} - Total"
                if col_name in data.columns:
                    grade_totals += data[col_name].sum()
        else:
            grade_totals = 0

        # Key metrics with enhanced styling
        st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(
                """
                <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
                    <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>📚 Total Students</p>
                    <h2 style='margin: 10px 0 0 0; color: white; font-size: 2em;'>{:,.0f}</h2>
                </div>
            """.format(
                    total_students
                ),
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #06d6a0 0%, #118ab2 100%);
                            border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(6, 214, 160, 0.3);'>
                    <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>✅ Pass Rate</p>
                    <h2 style='margin: 10px 0 0 0; color: white; font-size: 2em;'>{:.1f}%</h2>
                </div>
            """.format(
                    pass_rate_metric
                ),
                unsafe_allow_html=True,
            )

        with col3:
            avg_excellence = data["Excellence_Rate"].mean()
            st.markdown(
                """
                <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #ffd93d 0%, #ffb627 100%);
                            border-radius: 12px; color: #2d3436; box-shadow: 0 4px 12px rgba(255, 217, 61, 0.3);'>
                    <p style='margin: 0; font-size: 0.9em; opacity: 0.8;'>🌟 Division 1</p>
                    <h2 style='margin: 10px 0 0 0; color: #2d3436; font-size: 2em;'>{:.1f}%</h2>
                </div>
            """.format(
                    avg_excellence
                ),
                unsafe_allow_html=True,
            )
            st.caption(
                "📌 Percentage of students who scored Division 1 (highest performance grade)"
            )

        with col4:
            st.markdown(
                """
                <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #4c9aff 0%, #2684ff 100%);
                            border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(76, 154, 255, 0.3);'>
                    <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>🎓 Selected Grades</p>
                    <h2 style='margin: 10px 0 0 0; color: white; font-size: 2em;'>{:,.0f}</h2>
                </div>
            """.format(
                    grade_totals
                ),
                unsafe_allow_html=True,
            )

        with col5:
            if "Gender_Gap" in data.columns:
                avg_gender_gap = data["Gender_Gap"].mean()
                st.markdown(
                    """
                    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
                                border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(162, 155, 254, 0.3);'>
                        <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>👥 Gender Gap</p>
                        <h2 style='margin: 10px 0 0 0; color: white; font-size: 2em;'>{:.1f}%</h2>
                    </div>
                """.format(
                        avg_gender_gap
                    ),
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        # Tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
            [
                "📊 Overview",
                "🎯 Performance",
                "👥 Gender",
                "🏆 Rankings",
                "📈 Trends",
                "🗺️ Geography",
            ]
        )

        with tab1:
            show_overview(data, gender_filter, grade_filter)

        with tab2:
            show_performance(data, gender_filter)

        with tab3:
            show_gender_analysis(data, grade_filter)

        with tab4:
            show_rankings(data, gender_filter)

        with tab5:
            show_trends(data, gender_filter, grade_filter)

        with tab6:
            show_geographical_analysis(data)

    else:
        st.markdown(
            """
            <div style='text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
                        border-radius: 16px; margin: 40px 0; border: 2px solid #e8eaed;'>
                <h2 style='color: #5f6368; margin-bottom: 30px;'>
                    👈 Click 'Refresh Data' in the sidebar to start
                </h2>
                <div style='text-align: left; max-width: 600px; margin: 0 auto; color: #5f6368;'>
                    <h3 style='color: #667eea; margin-top: 30px;'>📝 Instructions:</h3>
                    <ol style='font-size: 1.1em; line-height: 1.8;'>
                        <li>The dashboard is pre-configured with your Google Sheet ID</li>
                        <li>Ensure the Google Sheet is publicly accessible</li>
                        <li>Click <strong>Refresh Data</strong> in the sidebar</li>
                        <li>Use filters to analyze specific districts</li>
                    </ol>
                    
                    <h3 style='color: #667eea; margin-top: 30px;'>📊 Available Analysis:</h3>
                    <ul style='font-size: 1.1em; line-height: 1.8;'>
                        <li><strong>Overview:</strong> Division distribution and summary statistics</li>
                        <li><strong>Performance:</strong> Trends and correlations</li>
                        <li><strong>Gender:</strong> Boys vs Girls comparison</li>
                        <li><strong>Rankings:</strong> Top and bottom performers</li>
                        <li><strong>Trends:</strong> Year-over-year analysis</li>
                    </ul>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )


def show_overview(data, gender_filter="All", grade_filter=None):
    """Overview tab"""
    st.markdown(
        "<h2 style='color: #5f6368; margin-top: 20px;'>📊 Performance Overview</h2>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        # Division distribution based on gender filter
        if gender_filter == "Boys Only":
            division_totals = {
                "Div 1": data["Division 1 - Boys"].sum(),
                "Div 2": data["Division 2 - Boys"].sum(),
                "Div 3": data["Division 3 - Boys"].sum(),
                "Div 4": data["Division 4 - Boys"].sum(),
                "Div U": data["Division U - Boys"].sum(),
                "Div X": data.get("Division X - Boys", pd.Series([0])).sum(),
            }
        elif gender_filter == "Girls Only":
            division_totals = {
                "Div 1": data["Division 1 - Girls"].sum(),
                "Div 2": data["Division 2 - Girls"].sum(),
                "Div 3": data["Division 3 - Girls"].sum(),
                "Div 4": data["Division 4 - Girls"].sum(),
                "Div U": data["Division U - Girls"].sum(),
                "Div X": data.get("Division X - Girls", pd.Series([0])).sum(),
            }
        else:
            division_totals = {
                "Div 1": data["Division 1 - Total"].sum(),
                "Div 2": data["Division 2 - Total"].sum(),
                "Div 3": data["Division 3 - Total"].sum(),
                "Div 4": data["Division 4 - Total"].sum(),
                "Div U": data["Division U - Total"].sum(),
                "Div X": data["Division X - Total"].sum(),
            }

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=list(division_totals.keys()),
                    values=list(division_totals.values()),
                    marker=dict(
                        colors=COLORS["chart_colors"], line=dict(color="white", width=2)
                    ),
                    hole=0.4,
                    textinfo="label+percent",
                    textfont=dict(size=16, color="#2d3436", family="Arial Black"),
                    textposition="auto",
                    insidetextorientation="radial",
                    hovertemplate="<b>%{label}</b><br>Count: %{value:,.0f}<br>Percent: %{percent}<extra></extra>",
                )
            ]
        )
        fig.update_layout(
            title=dict(
                text=f"<b>Division Distribution ({gender_filter})</b>",
                font=dict(size=20, color="#5f6368", family="Arial"),
            ),
            height=450,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#5f6368", size=13),
            showlegend=True,
            legend=dict(
                bgcolor="white",
                bordercolor="#e8eaed",
                borderwidth=1,
                font=dict(size=13, color="#5f6368"),
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Pass rate distribution
        fig = px.histogram(
            data,
            x="Pass_Rate",
            nbins=30,
            title="<b>Pass Rate Distribution</b>",
            labels={"Pass_Rate": "Pass Rate (%)", "count": "Districts"},
            color_discrete_sequence=[COLORS["info"]],
        )
        fig.update_layout(
            height=450,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#2d3436", size=13),
            title_font=dict(size=20, color="#5f6368", family="Arial"),
            xaxis=dict(
                showgrid=True,
                gridcolor="#f0f0f0",
                title_font=dict(size=14, color="#2d3436"),
                tickfont=dict(size=12, color="#2d3436"),
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#f0f0f0",
                title_font=dict(size=14, color="#2d3436"),
                tickfont=dict(size=12, color="#2d3436"),
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Top performers table
    st.markdown(
        "<h2 style='color: #5f6368; margin-top: 30px;'>🏆 Top 10 Performers</h2>",
        unsafe_allow_html=True,
    )
    top_10 = data.nlargest(10, "Pass_Rate")[
        ["District", "Pass_Rate", "Excellence_Rate", "Registered - Total"]
    ].copy()
    top_10["Pass_Rate"] = top_10["Pass_Rate"].apply(lambda x: f"{x:.1f}%")
    top_10["Excellence_Rate"] = top_10["Excellence_Rate"].apply(lambda x: f"{x:.1f}%")
    st.dataframe(top_10.reset_index(drop=True), use_container_width=True)

    # Registered vs Sat Analysis
    st.markdown("---")
    st.markdown(
        "<h2 style='color: #5f6368; margin-top: 30px;'>📋 Registration vs Examination Participation</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color: #80868b;'>Analysis of students who registered vs those who actually sat for the exam (Division X = Did not sit)</p>",
        unsafe_allow_html=True,
    )

    # Calculate sat vs not sat
    registered_total = data["Registered - Total"].sum()

    if "Division X - Total" in data.columns:
        did_not_sit = data["Division X - Total"].sum()
    else:
        did_not_sit = 0

    sat_for_exam = registered_total - did_not_sit
    participation_rate = (
        (sat_for_exam / registered_total * 100) if registered_total > 0 else 0
    )
    absentee_rate = (
        (did_not_sit / registered_total * 100) if registered_total > 0 else 0
    )

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
                <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>📝 Registered</p>
                <h2 style='margin: 10px 0 0 0; color: white; font-size: 2em;'>{registered_total:,}</h2>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #06d6a0 0%, #039770 100%);
                        border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(6, 214, 160, 0.3);'>
                <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>✅ Sat for Exam</p>
                <h2 style='margin: 10px 0 0 0; color: white; font-size: 2em;'>{sat_for_exam:,}</h2>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #ef476f 0%, #c9184a 100%);
                        border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(239, 71, 111, 0.3);'>
                <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>❌ Did Not Sit</p>
                <h2 style='margin: 10px 0 0 0; color: white; font-size: 2em;'>{did_not_sit:,}</h2>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #ffd93d 0%, #ffb627 100%);
                        border-radius: 12px; color: #2d3436; box-shadow: 0 4px 12px rgba(255, 217, 61, 0.3);'>
                <p style='margin: 0; font-size: 0.9em; opacity: 0.8;'>📊 Participation Rate</p>
                <h2 style='margin: 10px 0 0 0; color: #2d3436; font-size: 2em;'>{participation_rate:.1f}%</h2>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Pie chart
        participation_data = pd.DataFrame(
            {
                "Status": ["Sat for Exam", "Did Not Sit"],
                "Count": [sat_for_exam, did_not_sit],
            }
        )

        fig = px.pie(
            participation_data,
            values="Count",
            names="Status",
            title="<b>Examination Participation</b>",
            color="Status",
            color_discrete_map={"Sat for Exam": "#06d6a0", "Did Not Sit": "#ef476f"},
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(
            height=400,
            paper_bgcolor="white",
            font=dict(color="#2d3436", size=13),
            title_font=dict(size=20, color="#5f6368"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Bar chart by district (top 10 absentees)
        if "Division X - Total" in data.columns and "District" in data.columns:
            absentee_by_district = data[
                ["District", "Division X - Total", "Registered - Total"]
            ].copy()
            absentee_by_district["Absentee_Rate"] = (
                absentee_by_district["Division X - Total"]
                / absentee_by_district["Registered - Total"]
                * 100
            ).fillna(0)

            top_absentee = absentee_by_district.nlargest(10, "Division X - Total")

            fig = px.bar(
                top_absentee,
                x="District",
                y="Division X - Total",
                title="<b>Top 10 Districts by Absentees</b>",
                color="Absentee_Rate",
                color_continuous_scale="Reds",
                labels={
                    "Division X - Total": "Students Who Did Not Sit",
                    "Absentee_Rate": "Rate (%)",
                },
            )
            fig.update_layout(
                height=400,
                paper_bgcolor="white",
                font=dict(color="#2d3436", size=13),
                title_font=dict(size=20, color="#5f6368"),
                xaxis_tickangle=-45,
            )
            st.plotly_chart(fig, use_container_width=True)

    # Gender breakdown
    if "Division X - Boys" in data.columns and "Division X - Girls" in data.columns:
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            boys_absent = data["Division X - Boys"].sum()
            boys_registered = data["Registered - Boys"].sum()
            boys_sat = boys_registered - boys_absent
            boys_participation = (
                (boys_sat / boys_registered * 100) if boys_registered > 0 else 0
            )

            st.markdown("### 👦 Boys Participation")
            st.metric("Boys Who Sat", f"{boys_sat:,}", f"{boys_participation:.1f}%")
            st.metric(
                "Boys Absent", f"{boys_absent:,}", f"{100-boys_participation:.1f}%"
            )

        with col2:
            girls_absent = data["Division X - Girls"].sum()
            girls_registered = data["Registered - Girls"].sum()
            girls_sat = girls_registered - girls_absent
            girls_participation = (
                (girls_sat / girls_registered * 100) if girls_registered > 0 else 0
            )

            st.markdown("### 👧 Girls Participation")
            st.metric("Girls Who Sat", f"{girls_sat:,}", f"{girls_participation:.1f}%")
            st.metric(
                "Girls Absent", f"{girls_absent:,}", f"{100-girls_participation:.1f}%"
            )


def show_performance(data, gender_filter="All"):
    """Performance tab"""
    st.markdown(
        f"<h2 style='color: #5f6368; margin-top: 20px;'>🎯 Performance Analysis ({gender_filter})</h2>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        # Box plot
        fig = px.box(
            data,
            y="Pass_Rate",
            title="<b>Pass Rate Distribution</b>",
            labels={"Pass_Rate": "Pass Rate (%)"},
        )
        fig.update_traces(
            marker_color=COLORS["primary"], fillcolor=COLORS["primary"], opacity=0.7
        )
        fig.update_layout(
            height=450,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#2d3436", size=13),
            title_font=dict(size=20, color="#5f6368", family="Arial"),
            yaxis=dict(
                showgrid=True,
                gridcolor="#f0f0f0",
                title_font=dict(size=14, color="#2d3436"),
                tickfont=dict(size=12, color="#2d3436"),
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Scatter: Division 1 vs Pass Rate
        fig = px.scatter(
            data,
            x="Pass_Rate",
            y="Excellence_Rate",
            size="Registered - Total",
            title="<b>Division 1 vs Pass Rate</b>",
            labels={"Pass_Rate": "Pass Rate (%)", "Excellence_Rate": "Division 1 (%)"},
            color="Pass_Rate",
            color_continuous_scale="Viridis",
        )
        fig.update_traces(marker=dict(opacity=0.7, line=dict(width=0.5, color="white")))
        fig.update_layout(
            height=450,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#2d3436", size=13),
            title_font=dict(size=20, color="#5f6368", family="Arial"),
            xaxis=dict(
                showgrid=True,
                gridcolor="#f0f0f0",
                title_font=dict(size=14, color="#2d3436"),
                tickfont=dict(size=12, color="#2d3436"),
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#f0f0f0",
                title_font=dict(size=14, color="#2d3436"),
                tickfont=dict(size=12, color="#2d3436"),
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Performance categories
    data["Category"] = pd.cut(
        data["Pass_Rate"],
        bins=[0, 65, 75, 85, 95, 100],
        labels=["Needs Improvement", "Average", "Good", "Very Good", "Excellent"],
    )

    category_counts = data["Category"].value_counts().sort_index()

    fig = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        title="<b>Districts by Performance Category</b>",
        labels={"x": "Category", "y": "Number of Districts"},
        color=category_counts.index,
        color_discrete_map={
            "Excellent": COLORS["success"],
            "Very Good": COLORS["primary"],
            "Good": COLORS["warning"],
            "Average": COLORS["info"],
            "Needs Improvement": COLORS["danger"],
        },
    )
    fig.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#5f6368", size=12),
        title_font=dict(size=18, color="#5f6368"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
    )
    st.plotly_chart(fig, use_container_width=True)


def show_gender_analysis(data, grade_filter=None):
    """Gender analysis tab"""
    grade_text = f" - {', '.join(grade_filter)}" if grade_filter else ""
    st.markdown(
        f"<h2 style='color: #5f6368; margin-top: 20px;'>👥 Gender Performance Analysis{grade_text}</h2>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        # Gender comparison
        total_boys = data["Registered - Boys"].sum()
        total_girls = data["Registered - Girls"].sum()

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Boys", "Girls"],
                    values=[total_boys, total_girls],
                    marker=dict(
                        colors=[COLORS["boys"], COLORS["girls"]],
                        line=dict(color="white", width=2),
                    ),
                    hole=0.4,
                    textinfo="label+percent+value",
                    textfont=dict(size=16, color="white", family="Arial Black"),
                    textposition="auto",
                    hovertemplate="<b>%{label}</b><br>Count: %{value:,.0f}<br>Percent: %{percent}<extra></extra>",
                )
            ]
        )
        fig.update_layout(
            title=dict(
                text="<b>Total Registration by Gender</b>",
                font=dict(size=20, color="#5f6368", family="Arial"),
            ),
            height=450,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#5f6368", size=13),
            showlegend=True,
            legend=dict(
                bgcolor="white",
                bordercolor="#e8eaed",
                borderwidth=1,
                font=dict(size=13, color="#5f6368"),
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Gender gap distribution
        fig = px.histogram(
            data,
            x="Gender_Gap",
            nbins=30,
            title="<b>Gender Gap Distribution</b>",
            labels={"Gender_Gap": "Gender Gap (% points)"},
            color_discrete_sequence=[COLORS["primary"]],
        )
        fig.add_vline(
            x=0,
            line_dash="dash",
            line_color="#5f6368",
            line_width=2,
            annotation_text="Equal",
            annotation_position="top",
        )
        fig.update_layout(
            height=400,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#5f6368", size=12),
            title_font=dict(size=18, color="#5f6368"),
            xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
            yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Average pass rates by gender
    avg_boys = data["Boys_Pass_Rate"].mean()
    avg_girls = data["Girls_Pass_Rate"].mean()

    fig = go.Figure(
        data=[
            go.Bar(
                x=["Boys", "Girls"],
                y=[avg_boys, avg_girls],
                marker_color=[COLORS["boys"], COLORS["girls"]],
                text=[f"{avg_boys:.1f}%", f"{avg_girls:.1f}%"],
                textposition="outside",
                textfont=dict(size=16, color="#2d3436", family="Arial", weight="bold"),
                hovertemplate="<b>%{x}</b><br>Pass Rate: %{y:.1f}%<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        title=dict(
            text="<b>Average Pass Rate by Gender</b>",
            font=dict(size=18, color="#5f6368"),
        ),
        yaxis_title="Pass Rate (%)",
        height=400,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#5f6368", size=12),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        xaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True)


def show_rankings(data, gender_filter="All"):
    """Rankings tab"""
    st.markdown(
        f"<h2 style='color: #5f6368; margin-top: 20px;'>🏆 District Rankings ({gender_filter})</h2>",
        unsafe_allow_html=True,
    )

    metric = st.selectbox(
        "Select Ranking Metric:",
        [
            "Pass_Rate",
            "Excellence_Rate",
            "Division 1 - Total",
            "Strong_Performance_Rate",
        ],
        format_func=lambda x: x.replace("_", " ").title(),
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🥇 Top 15")
        top_15 = data.nlargest(15, metric)[["District", metric]]

        fig = px.bar(
            top_15.sort_values(metric),
            y="District",
            x=metric,
            orientation="h",
            title=f"<b>Top 15 by {metric.replace('_', ' ').title()}</b>",
            color=metric,
            color_continuous_scale=[[0, COLORS["success"]], [1, COLORS["primary"]]],
        )
        fig.update_layout(
            height=600,
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#5f6368", size=12),
            title_font=dict(size=18, color="#5f6368"),
            xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🔻 Bottom 15")
        bottom_15 = data.nsmallest(15, metric)[["District", metric]]

        fig = px.bar(
            bottom_15.sort_values(metric, ascending=False),
            y="District",
            x=metric,
            orientation="h",
            title=f"<b>Bottom 15 by {metric.replace('_', ' ').title()}</b>",
            color=metric,
            color_continuous_scale=[[0, COLORS["danger"]], [1, COLORS["warning"]]],
        )
        fig.update_layout(
            height=600,
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#5f6368", size=12),
            title_font=dict(size=18, color="#5f6368"),
            xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig, use_container_width=True)


def show_trends(data, gender_filter="All", grade_filter=None):
    """Trends analysis tab"""
    st.markdown(
        "<h2 style='color: #5f6368; margin-top: 20px;'>📈 Year-over-Year Trends Analysis</h2>",
        unsafe_allow_html=True,
    )

    if "Year" not in data.columns:
        st.warning("Year data not available in the dataset")
        return

    # Group by year for trend analysis
    yearly_data = (
        data.groupby("Year")
        .agg(
            {
                "Registered - Total": "sum",
                "Registered - Boys": "sum",
                "Registered - Girls": "sum",
                "Pass_Rate": "mean",
                "Boys_Pass_Rate": "mean",
                "Girls_Pass_Rate": "mean",
                "Excellence_Rate": "mean",
                "Division 1 - Total": "sum",
                "Division 2 - Total": "sum",
                "Division 3 - Total": "sum",
                "Division 4 - Total": "sum",
                "Division U - Total": "sum",
            }
        )
        .reset_index()
    )

    # Sort by year
    yearly_data = yearly_data.sort_values("Year")

    col1, col2 = st.columns(2)

    with col1:
        # Registration trends
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=yearly_data["Year"],
                y=yearly_data["Registered - Total"],
                mode="lines+markers",
                name="Total",
                line=dict(color=COLORS["primary"], width=3),
                marker=dict(size=10),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=yearly_data["Year"],
                y=yearly_data["Registered - Boys"],
                mode="lines+markers",
                name="Boys",
                line=dict(color=COLORS["boys"], width=2),
                marker=dict(size=8),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=yearly_data["Year"],
                y=yearly_data["Registered - Girls"],
                mode="lines+markers",
                name="Girls",
                line=dict(color=COLORS["girls"], width=2),
                marker=dict(size=8),
            )
        )
        fig.update_layout(
            title=dict(
                text="<b>Registration Trends Over Years</b>",
                font=dict(size=18, color="#5f6368"),
            ),
            xaxis_title="Year",
            yaxis_title="Number of Students",
            height=400,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#5f6368", size=12),
            hovermode="x unified",
            xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
            yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
            legend=dict(bgcolor="white", bordercolor="#e8eaed", borderwidth=1),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Pass rate trends
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=yearly_data["Year"],
                y=yearly_data["Pass_Rate"],
                mode="lines+markers",
                name="Overall",
                line=dict(color=COLORS["success"], width=3),
                marker=dict(size=10),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=yearly_data["Year"],
                y=yearly_data["Boys_Pass_Rate"],
                mode="lines+markers",
                name="Boys",
                line=dict(color=COLORS["boys"], width=2),
                marker=dict(size=8),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=yearly_data["Year"],
                y=yearly_data["Girls_Pass_Rate"],
                mode="lines+markers",
                name="Girls",
                line=dict(color=COLORS["girls"], width=2),
                marker=dict(size=8),
            )
        )
        fig.update_layout(
            title=dict(
                text="<b>Pass Rate Trends Over Years</b>",
                font=dict(size=18, color="#5f6368"),
            ),
            xaxis_title="Year",
            yaxis_title="Pass Rate (%)",
            height=400,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#5f6368", size=12),
            hovermode="x unified",
            xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
            yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
            legend=dict(bgcolor="white", bordercolor="#e8eaed", borderwidth=1),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Division 1 trend
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=yearly_data["Year"],
            y=yearly_data["Excellence_Rate"],
            mode="lines+markers",
            name="Division 1",
            line=dict(color=COLORS["primary"], width=3),
            marker=dict(size=10),
            fill="tozeroy",
            fillcolor="rgba(102, 126, 234, 0.15)",
        )
    )
    fig.update_layout(
        title=dict(
            text="<b>Division 1 Trend</b>",
            font=dict(size=18, color="#5f6368"),
        ),
        xaxis_title="Year",
        yaxis_title="Division 1 (%)",
        height=400,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#5f6368", size=12),
        xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Division distribution over years
    st.markdown(
        "<h2 style='color: #5f6368; margin-top: 30px;'>📊 Division Distribution by Year</h2>",
        unsafe_allow_html=True,
    )

    divisions_by_year = yearly_data[
        [
            "Year",
            "Division 1 - Total",
            "Division 2 - Total",
            "Division 3 - Total",
            "Division 4 - Total",
            "Division U - Total",
        ]
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=divisions_by_year["Year"],
            y=divisions_by_year["Division 1 - Total"],
            name="Division 1",
            marker_color=COLORS["chart_colors"][0],
        )
    )
    fig.add_trace(
        go.Bar(
            x=divisions_by_year["Year"],
            y=divisions_by_year["Division 2 - Total"],
            name="Division 2",
            marker_color=COLORS["chart_colors"][1],
        )
    )
    fig.add_trace(
        go.Bar(
            x=divisions_by_year["Year"],
            y=divisions_by_year["Division 3 - Total"],
            name="Division 3",
            marker_color=COLORS["chart_colors"][2],
        )
    )
    fig.add_trace(
        go.Bar(
            x=divisions_by_year["Year"],
            y=divisions_by_year["Division 4 - Total"],
            name="Division 4",
            marker_color=COLORS["chart_colors"][3],
        )
    )
    fig.add_trace(
        go.Bar(
            x=divisions_by_year["Year"],
            y=divisions_by_year["Division U - Total"],
            name="Division U",
            marker_color=COLORS["chart_colors"][4],
        )
    )
    fig.update_layout(
        title=dict(
            text="<b>Division Distribution by Year</b>",
            font=dict(size=18, color="#5f6368"),
        ),
        xaxis_title="Year",
        yaxis_title="Number of Students",
        barmode="stack",
        height=500,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#5f6368", size=12),
        hovermode="x unified",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        legend=dict(bgcolor="white", bordercolor="#e8eaed", borderwidth=1),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Year-over-Year growth rates
    st.markdown(
        "<h2 style='color: #5f6368; margin-top: 30px;'>📈 Year-over-Year Growth Analysis</h2>",
        unsafe_allow_html=True,
    )

    if len(yearly_data) > 1:
        growth_data = yearly_data.copy()
        growth_data["Registration Growth %"] = (
            growth_data["Registered - Total"].pct_change() * 100
        )
        growth_data["Pass Rate Change"] = growth_data["Pass_Rate"].diff()
        growth_data["Division 1 Change"] = growth_data["Excellence_Rate"].diff()

        col1, col2, col3 = st.columns(3)

        with col1:
            latest_growth = growth_data["Registration Growth %"].iloc[-1]
            st.metric(
                "Latest Registration Growth",
                f"{latest_growth:.1f}%" if not pd.isna(latest_growth) else "N/A",
                delta=f"{latest_growth:.1f}%" if not pd.isna(latest_growth) else None,
            )

        with col2:
            latest_pass_change = growth_data["Pass Rate Change"].iloc[-1]
            st.metric(
                "Latest Pass Rate Change",
                (
                    f"{latest_pass_change:.1f}%"
                    if not pd.isna(latest_pass_change)
                    else "N/A"
                ),
                delta=(
                    f"{latest_pass_change:.1f}%"
                    if not pd.isna(latest_pass_change)
                    else None
                ),
            )

        with col3:
            latest_excel_change = growth_data["Division 1 Change"].iloc[-1]
            st.metric(
                "Latest Division 1 Change",
                (
                    f"{latest_excel_change:.1f}%"
                    if not pd.isna(latest_excel_change)
                    else "N/A"
                ),
                delta=(
                    f"{latest_excel_change:.1f}%"
                    if not pd.isna(latest_excel_change)
                    else None
                ),
            )

        # Display growth table
        st.markdown(
            "<h2 style='color: #5f6368; margin-top: 30px;'>📊 Detailed Year-over-Year Comparison</h2>",
            unsafe_allow_html=True,
        )
        display_cols = [
            "Year",
            "Registered - Total",
            "Registration Growth %",
            "Pass_Rate",
            "Pass Rate Change",
            "Excellence_Rate",
            "Division 1 Change",
        ]
        display_data = growth_data[display_cols].round(2).copy()
        # Format percentage columns
        if "Registration Growth %" in display_data.columns:
            display_data["Registration Growth %"] = display_data[
                "Registration Growth %"
            ].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
        if "Pass_Rate" in display_data.columns:
            display_data["Pass_Rate"] = display_data["Pass_Rate"].apply(
                lambda x: f"{x:.1f}%"
            )
        if "Pass Rate Change" in display_data.columns:
            display_data["Pass Rate Change"] = display_data["Pass Rate Change"].apply(
                lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
            )
        if "Excellence_Rate" in display_data.columns:
            display_data["Excellence_Rate"] = display_data["Excellence_Rate"].apply(
                lambda x: f"{x:.1f}%"
            )
        if "Division 1 Change" in display_data.columns:
            display_data["Division 1 Change"] = display_data["Division 1 Change"].apply(
                lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
            )
        st.dataframe(display_data, use_container_width=True, hide_index=True)
    else:
        st.info("Need at least 2 years of data for growth analysis")

    # Data Explorer Section
    st.markdown("---")
    st.markdown(
        "<h2 style='color: #5f6368; margin-top: 30px;'>🔍 Data Explorer</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color: #80868b; margin-bottom: 20px;'>Search, filter, and export your data</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        search = st.text_input(
            "🔍 Search districts",
            "",
            placeholder="Type to search by district name...",
        )

    with col2:
        sort_by = st.selectbox(
            "Sort by",
            ["Pass_Rate", "Registered - Total", "Excellence_Rate", "District"],
            index=0,
        )

    # Filter data based on search
    filtered_data = data.copy()
    if search and "District" in filtered_data.columns:
        filtered_data = filtered_data[
            filtered_data["District"].str.contains(search, case=False, na=False)
        ]

    # Column selector
    available_cols = filtered_data.columns.tolist()
    default_cols = [
        col
        for col in ["District", "Pass_Rate", "Excellence_Rate", "Registered - Total"]
        if col in available_cols
    ]

    cols_to_show = st.multiselect(
        "📋 Select columns to display",
        available_cols,
        default=default_cols[: min(4, len(default_cols))],
    )

    if cols_to_show:
        # Sort and display data
        if sort_by in filtered_data.columns:
            display_data = (
                filtered_data[cols_to_show]
                .sort_values(sort_by, ascending=False)
                .reset_index(drop=True)
            )
        else:
            display_data = filtered_data[cols_to_show].reset_index(drop=True)

        # Show record count
        st.markdown(
            f"<p style='color: #80868b;'>Showing {len(display_data):,} of {len(data):,} records</p>",
            unsafe_allow_html=True,
        )

        # Calculate stats before formatting (need numeric values)
        stats_data = display_data.copy()

        # Format percentage columns for display
        display_data = display_data.copy()
        if "Pass_Rate" in display_data.columns:
            display_data["Pass_Rate"] = display_data["Pass_Rate"].apply(
                lambda x: f"{x:.1f}%"
            )
        if "Excellence_Rate" in display_data.columns:
            display_data["Excellence_Rate"] = display_data["Excellence_Rate"].apply(
                lambda x: f"{x:.1f}%"
            )
        if "Boys_Pass_Rate" in display_data.columns:
            display_data["Boys_Pass_Rate"] = display_data["Boys_Pass_Rate"].apply(
                lambda x: f"{x:.1f}%"
            )
        if "Girls_Pass_Rate" in display_data.columns:
            display_data["Girls_Pass_Rate"] = display_data["Girls_Pass_Rate"].apply(
                lambda x: f"{x:.1f}%"
            )

        # Display dataframe with custom styling
        st.dataframe(
            display_data,
            use_container_width=True,
            height=400,
            hide_index=False,
        )

        # Export options
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            csv = display_data.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"ple_data_filtered_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )

        with col2:
            try:
                from io import BytesIO

                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                    display_data.to_excel(writer, index=False, sheet_name="PLE Data")
                excel_data = excel_buffer.getvalue()

                st.download_button(
                    label="📊 Download as Excel",
                    data=excel_data,
                    file_name=f"ple_data_filtered_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            except ImportError:
                st.info("📊 Excel export requires openpyxl. Use CSV export instead.")

        # Quick stats about filtered data (use numeric stats_data)
        if len(stats_data) > 0:
            st.markdown("---")
            st.markdown("### 📈 Quick Stats (Filtered Data)")

            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

            with stat_col1:
                if "Registered - Total" in stats_data.columns:
                    st.metric(
                        "Total Students",
                        f"{stats_data['Registered - Total'].sum():,.0f}",
                    )

            with stat_col2:
                if "Pass_Rate" in stats_data.columns:
                    st.metric(
                        "Avg Pass Rate",
                        f"{stats_data['Pass_Rate'].mean():.1f}%",
                    )

            with stat_col3:
                if "Excellence_Rate" in stats_data.columns:
                    st.metric(
                        "Avg Division 1",
                        f"{stats_data['Excellence_Rate'].mean():.1f}%",
                    )

            with stat_col4:
                st.metric("Districts", len(stats_data))
    else:
        st.info("👆 Please select at least one column to display")


def show_geographical_analysis(data):
    """Geographical analysis tab"""
    st.markdown(
        "<h2 style='color: #5f6368; margin-top: 20px;'>🗺️ Geographical Performance Analysis</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color: #80868b;'>Regional and zonal performance breakdown with pass and failure rates</p>",
        unsafe_allow_html=True,
    )

    # Calculate failure rate
    data_with_failure = data.copy()
    data_with_failure["Failure_Rate"] = 100 - data_with_failure["Pass_Rate"]

    # Check which geographical columns are available
    has_sub_region = "Sub Region" in data.columns
    has_zone = "Zone" in data.columns
    has_district = "District" in data.columns

    # Sub Region Analysis
    if has_sub_region:
        st.markdown("---")
        st.markdown("### 📍 Performance by Sub Region")

        regional_stats = (
            data_with_failure.groupby("Sub Region")
            .agg(
                {
                    "Registered - Total": "sum",
                    "Pass_Rate": "mean",
                    "Excellence_Rate": "mean",
                    "Failure_Rate": "mean",
                }
            )
            .reset_index()
        )

        regional_stats = regional_stats.sort_values("Pass_Rate", ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            # Pass Rate by Sub Region
            fig = px.bar(
                regional_stats,
                x="Sub Region",
                y="Pass_Rate",
                title="<b>Pass Rate by Sub Region</b>",
                color="Pass_Rate",
                color_continuous_scale="Greens",
                labels={"Pass_Rate": "Pass Rate (%)"},
                text="Pass_Rate",
            )
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig.update_layout(
                height=450,
                paper_bgcolor="white",
                font=dict(color="#2d3436", size=13),
                title_font=dict(size=20, color="#5f6368"),
                xaxis_tickangle=-45,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Failure Rate by Sub Region
            fig = px.bar(
                regional_stats,
                x="Sub Region",
                y="Failure_Rate",
                title="<b>Failure Rate by Sub Region</b>",
                color="Failure_Rate",
                color_continuous_scale="Reds",
                labels={"Failure_Rate": "Failure Rate (%)"},
                text="Failure_Rate",
            )
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig.update_layout(
                height=450,
                paper_bgcolor="white",
                font=dict(color="#2d3436", size=13),
                title_font=dict(size=20, color="#5f6368"),
                xaxis_tickangle=-45,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        # Regional comparison table
        st.markdown("#### 📊 Regional Performance Summary")
        regional_display = regional_stats.copy()
        regional_display["Pass_Rate"] = regional_display["Pass_Rate"].apply(
            lambda x: f"{x:.1f}%"
        )
        regional_display["Failure_Rate"] = regional_display["Failure_Rate"].apply(
            lambda x: f"{x:.1f}%"
        )
        regional_display["Excellence_Rate"] = regional_display["Excellence_Rate"].apply(
            lambda x: f"{x:.1f}%"
        )
        regional_display.columns = [
            "Sub Region",
            "Total Students",
            "Pass Rate",
            "Division 1",
            "Failure Rate",
        ]
        st.dataframe(regional_display, use_container_width=True, hide_index=True)

    # District-level heatmap
    if has_district:
        st.markdown("---")
        st.markdown("### 🗺️ District Performance Heatmap")

        col1, col2 = st.columns(2)

        with col1:
            # Top 20 districts by pass rate
            top_districts = data_with_failure.nlargest(20, "Pass_Rate")[
                ["District", "Pass_Rate", "Failure_Rate"]
            ]

            fig = px.bar(
                top_districts,
                x="Pass_Rate",
                y="District",
                orientation="h",
                title="<b>Top 20 Districts by Pass Rate</b>",
                color="Pass_Rate",
                color_continuous_scale="Greens",
                labels={"Pass_Rate": "Pass Rate (%)"},
            )
            fig.update_layout(
                height=600,
                paper_bgcolor="white",
                font=dict(color="#2d3436", size=11),
                title_font=dict(size=18, color="#5f6368"),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Bottom 20 districts by pass rate (highest failure)
            bottom_districts = data_with_failure.nsmallest(20, "Pass_Rate")[
                ["District", "Pass_Rate", "Failure_Rate"]
            ]

            fig = px.bar(
                bottom_districts,
                x="Failure_Rate",
                y="District",
                orientation="h",
                title="<b>Top 20 Districts by Failure Rate</b>",
                color="Failure_Rate",
                color_continuous_scale="Reds",
                labels={"Failure_Rate": "Failure Rate (%)"},
            )
            fig.update_layout(
                height=600,
                paper_bgcolor="white",
                font=dict(color="#2d3436", size=11),
                title_font=dict(size=18, color="#5f6368"),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

    # Geographic scatter plot
    st.markdown("---")
    st.markdown("### 📊 Performance Distribution")

    if has_sub_region or has_zone:
        color_col = "Sub Region" if has_sub_region else "Zone"

        fig = px.scatter(
            data_with_failure,
            x="Pass_Rate",
            y="Failure_Rate",
            size="Registered - Total",
            color=color_col,
            hover_data=["District"] if has_district else None,
            title=f"<b>Pass Rate vs Failure Rate by {color_col}</b>",
            labels={"Pass_Rate": "Pass Rate (%)", "Failure_Rate": "Failure Rate (%)"},
        )
        fig.update_layout(
            height=500,
            paper_bgcolor="white",
            font=dict(color="#2d3436", size=13),
            title_font=dict(size=20, color="#5f6368"),
        )
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
