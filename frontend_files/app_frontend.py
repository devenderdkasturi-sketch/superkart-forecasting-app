import streamlit as st
import requests
import pandas as pd
import io

# 1. Configure the structural landing layout look of the dashboard app
st.set_page_config(
    page_title="SuperKart Quarter Sales Forecasting Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Establish dynamic routing network targets configurations
BACKEND_URL = "http://backend:7860"

st.title("🛒 SuperKart Inventory & Sales Forecast Terminal")
st.markdown("---")

# Setup sidebar navigational control panels maps
st.sidebar.header("🛠️ Forecast Mode Configuration")
mode = st.sidebar.radio("Select Prediction Tier", ["Real-time Online Entry", "Bulk File Dataset Stream Processing"])

if mode == "Real-time Online Entry":
    st.subheader("💡 Single Record Vector Parameters Input Matrix")
    
    # Arrange forms columns arrays evenly for field selections layout grids
    col1, col2, col3 = st.columns(3)
    
    with col1:
        product_mrp = st.number_input("Product Maximum Retail Price (MRP)", min_value=1.0, max_value=500.0, value=117.08, step=0.01)
        product_weight = st.number_input("Product Weight", min_value=0.1, max_value=50.0, value=12.66, step=0.01)
        store_age = st.slider("Store Age (Years)", min_value=1, max_value=50, value=16)

    with col2:
        product_area = st.number_input("Display Allocated Area Ratio", min_value=0.0, max_value=1.0, value=0.027, format="%.4f")
        sugar_content = st.selectbox("Product Sugar Content Category", ["Low Sugar", "Regular", "No Sugar"])
        prod_id_char = st.selectbox("Product Identification Prefix", ["FD", "DR", "NC"])

    with col3:
        store_size = st.selectbox("Store Size Footprint Segment", ["Small", "Medium", "High"])
        city_type = st.selectbox("Store Location Urban Density City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Operational Framework Format Type", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Departmental Store", "Food Mart"])
        category = st.selectbox("Product Type Category Profile", ["Perishables", "Non Perishables"])

    # Package unified structural features dictionary map payload tracking inputs
    payload = {
        "Product_Weight": float(product_weight),
        "Product_Sugar_Content": sugar_content,
        "Product_Allocated_Area": float(product_area),
        "Product_MRP": float(product_mrp),
        "Store_Size": store_size,
        "Store_Location_City_Type": city_type,
        "Store_Type": store_type,
        "Product_Id_char": prod_id_char,
        "Store_Age_Years": int(store_age),
        "Product_Type_Category": category
    }

    if st.button("🚀 Calculate Real-time Forecast", type="primary"):
        with st.spinner("Streaming operational query data vectors to analytics model..."):
            try:
                response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload)
                if response.status_code == 200:
                    prediction = response.json()["prediction"]
                    st.success(f"📈 Estimated Expected Quarter Sales Target Revenue: **${prediction:,.2f}**")
                else:
                    st.error(f"❌ Processing Error Boundary Triggered. Backend Response Code: {response.status_code}")
            except Exception as e:
                st.error(f"🔌 Connection Bottleneck: Could not bridge backend microservice network. Details: {e}")

else:
    st.subheader("📂 Bulk Operational Dataset Matrix Stream Upload Processing")
    st.markdown("Provide bulk logistics pipeline sheets in standard comma-separated text formatting layout structures (.csv).")
    
    uploaded_file = st.file_uploader("Choose csv document stream...", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # Preview user data tables properties parameters ahead of estimation pipelines
            preview_df = pd.read_csv(uploaded_file)
            st.write("📊 Uploaded Input Records Matrix Preview (First 5 Rows):")
            st.dataframe(preview_df.head(5))
            
            # Reset file read handle marker after previewing
            uploaded_file.seek(0)
            
            if st.button("📦 Process Bulk Dataset Optimization Predictions", type="primary"):
                with st.spinner("Streaming data sheets safely through optimization filters..."):
                    files_payload = {'file': (uploaded_file.name, uploaded_file.read(), 'text/csv')}
                    
                    response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files_payload)
                    
                    if response.status_code == 200:
                        results_dict = response.json()
                        
                        # Stitch structural batch output vectors back onto user data tracking frames
                        output_df = preview_df.copy()
                        output_df["Predicted_Outlet_Sales_Total"] = output_df.index.map(lambda i: results_dict.get(str(i), 0.0))
                        
                        st.success("🎉 Bulk batch processing calculations finished successfully!")
                        st.subheader("🎯 Integrated Output Forecast Estimation Insights Metrics Matrix:")
                        st.dataframe(output_df)
                        
                        # Export compiled final dataset results spreadsheet downstream
                        csv_buffer = io.BytesIO()
                        output_df.to_csv(csv_buffer, index=False)
                        st.download_button(
                            label="📥 Export Result Mapping Spreadsheet Spreadsheet (.csv)",
                            data=csv_buffer.getvalue(),
                            file_name="SuperKart_Quarter_Sales_Predictions.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error(f"❌ Batch pipeline mapping server fault occurred. Status: {response.status_code}")
        except Exception as e:
            st.error(f"⚠️ Structural validation layout configuration error: {e}")