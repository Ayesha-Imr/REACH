import os
from docling.document_converter import DocumentConverter
import xml.etree.ElementTree as ET
from typing import List
from typing import Union
from urllib.parse import urljoin
import streamlit as st
import requests
import tempfile
from io import BytesIO
from docling.datamodel.base_models import DocumentStream

def get_sitemap_urls(base_url: str, sitemap_filename: str = "sitemap.xml") -> List[str]:
    """Fetches and parses a sitemap XML file to extract URLs.

    Args:
        base_url: The base URL of the website
        sitemap_filename: The filename of the sitemap (default: sitemap.xml)

    Returns:
        List of URLs found in the sitemap. If sitemap is not found, returns a list
        containing only the base URL.

    Raises:
        ValueError: If there's an error fetching (except 404) or parsing the sitemap
    """
    try:
        sitemap_url = urljoin(base_url, sitemap_filename)

        # Fetch sitemap URL
        response = requests.get(sitemap_url, timeout=10)

        # # Return just the base URL if sitemap not found
        if response.status_code == 404:
            return [base_url.rstrip("/")]

        response.raise_for_status()

        # Parse XML content
        root = ET.fromstring(response.content)

        # Handle different XML namespaces that sitemaps might use
        namespaces = (
            {"ns": root.tag.split("}")[0].strip("{")} if "}" in root.tag else ""
        )

        # Extract URLs using namespace if present
        if namespaces:
            urls = [elem.text for elem in root.findall(".//ns:loc", namespaces)]
        else:
            urls = [elem.text for elem in root.findall(".//loc")]

        return urls

    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch sitemap: {str(e)}")
    except ET.ParseError as e:
        raise ValueError(f"Failed to parse sitemap XML: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error processing sitemap: {str(e)}")


# Initialize the DocumentConverter once for reuse
converter = DocumentConverter()


# --------------------------------------------------------------
# Basic URL extraction
# --------------------------------------------------------------
def url_extract(pdf_url):
    result = converter.convert(pdf_url) # https://arxiv.org/pdf/2408.09869"
    document = result.document
    markdown_output = document.export_to_markdown()
    print("PDF Extraction (URL):")
    print(markdown_output)
    return markdown_output

# --------------------------------------------------------------
# Scrape multiple pages using the sitemap
# --------------------------------------------------------------
def scrape_sitemap(sitemap_url):
    sitemap_urls = get_sitemap_urls(sitemap_url) # https://ds4sd.github.io/docling/sitemap.xml
    conv_results_iter = converter.convert_all(sitemap_urls)
    docs = []
    for result in conv_results_iter:
        if result.document:
            docs.append(result.document.export_to_markdown())
    print(f"Scraped {len(docs)} documents using the sitemap.")


# --------------------------------------------------------------
# File upload
# --------------------------------------------------------------
def file_local_extract(file: Union[str, st.runtime.uploaded_file_manager.UploadedFile]):
    if isinstance(file, str):
        # Existing functionality for local file paths
        if os.path.exists(file):
            result = converter.convert(file)
            document = result.document
            return document.export_to_markdown()
        else:
            return "File not found."

    elif isinstance(file, st.runtime.uploaded_file_manager.UploadedFile):
        try:
            # Wrap the UploadedFile in a DocumentStream
            file_stream = BytesIO(file.getbuffer())
            doc_stream = DocumentStream(name=file.name, stream=file_stream)
            result = converter.convert(doc_stream)
            document = result.document
            return document.export_to_markdown() if document else "No text extracted."

        except Exception as e:
            return f"Error processing file: {str(e)}"

    else:
        return "Unsupported file type."