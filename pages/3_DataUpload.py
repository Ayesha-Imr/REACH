import streamlit as st
from backend import main
from streamlit import session_state

st.set_page_config(page_title="Data Upload", page_icon="📤")

st.title("Upload Data")

if 'user_id' not in session_state:
    st.warning("Please log in or sign up first.")
else:
    webpage_url = st.text_input("Enter Webpage URL")
    website_url = st.text_input("Enter Website URL")
    uploaded_file = st.file_uploader("Upload a file (PDF/DOCX)", type=["pdf", "docx"])

    if st.button("Submit"):
        with st.spinner("Extracting data..."):
            extracted_texts = []
            if webpage_url:
                extracted_texts.append(main.url_extraction(webpage_url))
            if website_url:
                extracted_texts.append(main.sitemap_extract(website_url))
            if uploaded_file:
                extracted_texts.append(main.local_extract(uploaded_file))

            combined_text = ' '.join(extracted_texts)
            print(combined_text)
            summary_text = main.summary(combined_text)

        with st.spinner("Creating chunks..."):
            chunked_texts = []
            for text in extracted_texts:
                chunked_texts.append(main.create_chunks(text, chunk_size=200, overlap_size=30))

        with st.spinner("Adding data to vector database..."):
            for i, text in enumerate(extracted_texts):
                source = webpage_url if i == 0 else website_url if i == 1 else uploaded_file.name
                chunks_list = main.chunks_list(chunked_texts[i], source, summary_text)
                main.insert_data(chunks_list, session_state.user_id)

        st.success("Data uploaded and processed successfully!")
