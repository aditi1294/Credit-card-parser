import streamlit as st
import json
from dataclasses import asdict
from parser.parser import StatementParser
import time

# Page config with custom styling
st.set_page_config(
    page_title="Credit Card Statement Parser", 
    page_icon="💳", 
    layout="centered"
)

# Custom CSS for enhanced animations and styling
st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Card-like container */
    .stApp {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Header styling */
    h1 {
        color: #000 !important;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        animation: slideIn 0.6s ease-out;
        letter-spacing: -1px;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #000;
        font-size: 1.1rem;
        margin-top: -1rem;
        margin-bottom: 2rem;
        animation: slideIn 0.8s ease-out;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #000 !important;
        animation: fadeIn 1s ease-out;
    }
    
    [data-testid="stMetricLabel"] {
        color: #000 !important;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* Upload area enhancement */
    [data-testid="stFileUploader"] {
        border: 3px dashed #667eea;
        border-radius: 15px;
        padding: 2.5rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: pulse 2s ease-in-out infinite;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2;
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: none;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(118, 75, 162, 0.12) 100%);
    }
    
    [data-testid="stFileUploader"] label {
        color: #000 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Button styling */
    /* Download Button styling */
.stDownloadButton button {
    background-color: black !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 1rem 2rem !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.stDownloadButton button:hover {
    background-color: #333 !important; /* darker black on hover */
    color: white !important;
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}   
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        animation: fadeIn 1s ease-out;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Info/Success boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid #667eea;
        animation: slideIn 0.5s ease-out;
        background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, transparent 100%);
    }
    
    .stAlert > div {
        color: #000 !important;
        font-weight: 500;
    }
    
    /* Subheader styling */
    h3 {
        color: #000 !important;
        font-weight: 700;
        margin-top: 2.5rem !important;
        margin-bottom: 1.5rem !important;
        font-size: 1.5rem !important;
        animation: slideIn 0.7s ease-out;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        display: inline-block;
    }
    
    /* Metric container */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease-out;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    /* Progress bar animation */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        animation: shimmer 2s infinite;
        background-size: 1000px 100%;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
        border-radius: 10px;
        color: #000 !important;
        font-weight: 600;
    }
    
    /* Empty state styling */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-radius: 20px;
        border: 3px dashed #667eea;
        animation: fadeIn 1s ease-out;
        transition: all 0.3s ease;
    }
    
    .empty-state:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    
    .empty-state h2 {
        color: #000;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    
    .empty-state p {
        color: #000;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    .empty-state ul {
        list-style: none;
        padding: 0;
        margin-top: 2rem;
    }
    
    .empty-state li {
        margin: 1rem 0;
        font-size: 1.05rem;
        color: #000;
        font-weight: 500;
        animation: slideIn 1s ease-out;
        animation-fill-mode: both;
    }
    
    .empty-state li:nth-child(1) { animation-delay: 0.2s; }
    .empty-state li:nth-child(2) { animation-delay: 0.3s; }
    .empty-state li:nth-child(3) { animation-delay: 0.4s; }
    .empty-state li:nth-child(4) { animation-delay: 0.5s; }
    .empty-state li:nth-child(5) { animation-delay: 0.6s; }
    
    /* Badge styling */
    .transaction-badge {
        display: inline-block;
        background: black;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        margin-bottom: 1.5rem;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #000;
        font-size: 0.95rem;
        margin-top: 3rem;
        font-weight: 500;
        animation: fadeIn 1.5s ease-out;
    }
    
    /* Column animations */
    [data-testid="column"] {
        animation: fadeIn 0.8s ease-out;
    }
    
    [data-testid="column"]:nth-child(1) { animation-delay: 0.1s; }
    [data-testid="column"]:nth-child(2) { animation-delay: 0.2s; }
    [data-testid="column"]:nth-child(3) { animation-delay: 0.3s; }
</style>
""", unsafe_allow_html=True)

# Header with animation
st.title("Credit Card Statement Parser")
st.markdown(
    "<p class='subtitle'>Extract key financial details from your statements in seconds</p>", 
    unsafe_allow_html=True
)

# Upload section
st.markdown("<br>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop your PDF here or click to browse", 
    type=["pdf"],
    help="Upload your credit card statement in PDF format"
)

if uploaded_file is not None:
    # Progress indicator
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.info("Analyzing document structure...")
    progress_bar.progress(25)
    time.sleep(0.4)
    
    # Save uploaded file temporarily
    temp_path = "temp_statement.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())
    
    status_text.info("Extracting financial data...")
    progress_bar.progress(50)
    time.sleep(0.3)
    
    parser = StatementParser()
    result = parser.parse(temp_path)
    result_dict = asdict(result)
    result_dict["transactions"] = [asdict(t) for t in result.transactions]
    
    status_text.info("Processing transactions...")
    progress_bar.progress(75)
    time.sleep(0.4)
    
    progress_bar.progress(100)
    status_text.success("Parsing completed successfully")
    time.sleep(0.6)
    
    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()
    
    # Summary section
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Statement Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Issuer", result.issuer or "N/A")
        st.metric("Card Last 4", result.last4 or "N/A")
    with col2:
        st.metric("Billing Cycle", result.billing_cycle or "N/A")
        st.metric("Due Date", result.due_date or "N/A")
    with col3:
        balance_value = f"${result.total_balance:,.2f}" if result.total_balance else "N/A"
        st.metric("Total Balance", balance_value)
    
    # Transactions section
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Transaction History")
    
    if result.transactions:
        # Transaction count badge
        st.markdown(
            f"<div class='transaction-badge'>{len(result.transactions)} transactions found</div>", 
            unsafe_allow_html=True
        )
        
        tx_table = [
            {
                "Date": t.date, 
                "Description": t.description, 
                "Amount": f"${t.amount:,.2f}" if isinstance(t.amount, (int, float)) else t.amount
            }
            for t in result.transactions
        ]
        st.dataframe(tx_table, use_container_width=True, hide_index=True)
    else:
        st.warning("No transactions detected in this statement")
    
    # Expandable JSON section
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("View Raw JSON Data", expanded=False):
        st.json(result_dict)
    
    # Download button
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="Download Results as JSON",
        data=json.dumps(result_dict, indent=2),
        file_name=f"parsed_statement_{uploaded_file.name.replace('.pdf', '')}.json",
        mime="application/json",
        use_container_width=True
    )
    
else:
    # Empty state
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='empty-state'>
        <h2>Get Started</h2>
        <p>Upload your credit card statement PDF above to extract</p>
        <ul>
            <li> • Issuer information</li>
            <li> • Card details</li>
            <li> • Billing cycle and due dates</li>
            <li> • Balance information</li>
            <li> • Complete transaction history</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
