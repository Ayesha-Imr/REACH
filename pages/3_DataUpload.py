import streamlit as st
from backend import main
from streamlit import session_state

# Set up page configuration
st.set_page_config(page_title="Data Upload", page_icon="📤", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
            margin-bottom: -10px;
        }
        .subtitle {
            font-size: 18px;
            color: #555;
            text-align: center;
            margin-bottom: 30px;
        }
        .upload-container {
            background-color: #f9f9f9;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: 0 auto;
        }
        .button {
            width: 100%;
            background-color: #2C3E50;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
        }
        .error, .success {
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title
st.markdown('<h1 class="title">📤 Upload Your Startup Data</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Help REACH understand your startup better to provide tailored market insights.</p>', unsafe_allow_html=True)

# Authentication Check
if 'user_id' not in session_state:
    st.warning("⚠️ Please log in or sign up first to proceed.")
    st.stop()  # Prevents further execution if the user is not logged in

# Instructions
st.markdown(
    """
    ### 📌 **Instructions**
    - **Webpage URL:** Provide a **specific page** from your startup’s site (e.g., About Us, Product Page).
    - **Website URL:** Enter your **main website URL** if you want REACH to extract data from all indexed pages.
    - **Upload a File:** Upload your **pitch deck** or other startup documents **(PDF/DOCX, max 2MB).**
    """,
    unsafe_allow_html=True
)

# Data Input Fields
with st.container():  # Ensures proper spacing and avoids blank boxes
    webpage_url = st.text_input("🔗 Enter Webpage URL", placeholder="e.g., https://example.com/about", autocomplete="off", help="Provide the URL of a specific webpage related to your startup.")
    website_url = st.text_input("🌐 Enter Website URL", placeholder="e.g., https://example.com", autocomplete="off", help="Provide the main website URL for broader data extraction.")
    uploaded_file = st.file_uploader("📂 Upload a File (PDF/DOCX)", type=["pdf", "docx"], help="Upload your pitch deck or any other relevant document. Ensure the file size is below 2MB.")

# Submit Button
if st.button("🚀 Submit Data", key="submit_data", help="Click to process and upload your data"):
    if not (webpage_url or website_url or uploaded_file):
        st.error("⚠️ Please provide at least one data source (URL or file).")
    else:
        with st.spinner("🔍 Extracting data... Please wait"):
            extracted_texts = []
            
            if webpage_url:
                extracted_texts.append(main.url_extraction(webpage_url))
            if website_url:
                extracted_texts.append(main.sitemap_extract(website_url))
            if uploaded_file:
                extracted_texts.append(main.local_extract(uploaded_file))

            combined_text = ' '.join(extracted_texts)
            summary_text = main.summary(combined_text)

        with st.spinner("📊 Creating data chunks..."):
            chunked_texts = []
            for text in extracted_texts:
                chunked_texts.append(main.create_chunks(text, chunk_size=200, overlap_size=30))

        with st.spinner("🗄️ Storing data in vector database..."):
            for i, text in enumerate(extracted_texts):
                source = webpage_url if i == 0 else website_url if i == 1 else uploaded_file.name
                chunks_list = main.chunks_list(chunked_texts[i], source, summary_text)
                main.insert_data(chunks_list, session_state.user_id)

        st.success("✅ Data uploaded and processed successfully!")

        # Displaying the generated summary text with a clear heading
        st.markdown("## 🏢 **Your Startup Description**")
        st.info(summary_text)
