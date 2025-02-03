import sys
import os
import streamlit as st

# Adjust path to import agent module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agent')))
from ai_agent import handle_query

# Set Streamlit page config
st.set_page_config(page_title="AI-Powered Business Insights Agent", layout="wide")

# --- Apply Global CSS ---
st.markdown(
    """
    <style>
        /* Main Title */
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #4A90E2;
            margin-bottom: 5px;
        }
        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #666;
            margin-bottom: 20px;
        }
        /* Input Field */
        .stTextInput>div>div>input {
            font-size: 18px;
            padding: 10px;
        }
        /* Button Styling */
        .stButton>button {
            font-size: 18px;
            font-weight: bold;
            background-color: #4A90E2;
            color: white;
            border-radius: 8px;
            padding: 12px 24px;
            transition: 0.3s;
        }
        /* Button Hover Effect */
        .stButton>button:hover {
            background-color: #4A90E2;
            box-shadow: 0px 0px 10px #4A90E2;
        }
        .stButton>button:focus {
            border: 2px solid #4A90E2 !important;
            color: white !important;
        }
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
            padding: 20px;
        }
        .sidebar-title {
            font-size: 30px;
            font-weight: bold;
            color: #4A90E2;
            text-align: left ;           
            margin-bottom: 10px;
        }
        .sidebar-description {
            font-size: 14px;
            color: #555;
            text-align: left;
        }
        /* Output Styling */
        .output {
            font-size: 16px;
            color: #4A90E2;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar Section ---
st.sidebar.markdown('<div class="sidebar-title" >AI-Powered Insights</div>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-description">Ask business-related queries and get AI-driven insights.</p>', unsafe_allow_html=True)

# --- Main Title ---
st.markdown('<div class="title">AI-Powered Business Insights Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask a question about business metrics and get instant insights!</div>', unsafe_allow_html=True)

# --- Query Input ---
user_query = st.text_input(" Enter your business query:", placeholder="Enter your business query here...")

# --- Submit Button ---
if st.button("Generate Insights"):
    if user_query:
        with st.spinner("🔍 Analyzing data... Please wait!"):
            try:
                result = handle_query(user_query)
                if not result:
                    st.warning("No insights found for your query. Try refining it.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        
        # --- Display Result ---
        if isinstance(result, list):
            if isinstance(result[0], dict):
                st.success("✅ Here's your insight:")
                st.dataframe(result)  # Show as a table if structured data
            else:
                st.markdown("<p class='output'><strong>Insight:</strong></p>", unsafe_allow_html=True)
                for res in result:
                    st.markdown(f"<p class='output'>- {res}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p class='output'>{result}</p>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a query to get insights.")




