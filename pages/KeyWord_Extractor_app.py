import streamlit as st
from keybert import KeyBERT
from PyPDF2 import PdfReader

# Set page layout to wide
st.set_page_config(layout="wide")

@st.cache_resource
def key_extract(text, maxlength=None):
    """
    Function to extract keywords from text.

    Args:
        text (str): The input text from which keywords need to be extracted.
        maxlength (int, optional): Maximum length of the extracted keywords. Defaults to None.

    Returns:
        str: Extracted keywords from the text.
    """
    content = "Keywords: "  
    for keyword, _ in text:
        content = content + ", " + keyword
    return content

def key_extract_from_pdf(file_path):
    """
    Function to extract text from PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF file.
    """
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        page = reader.pages[0]
        text = page.extract_text()
    return text

def app():
    # Title
    st.title('KEYWORD EXTRACTOR')

    model = KeyBERT()

    # Sidebar choice
    choice = st.sidebar.selectbox("Select your choice", ["Keyword Extraction from Text", "Keyword Extraction from Document"])

    if choice == "Keyword Extraction from Text":
        # Text input for keyword extraction
        st.subheader("Extract Keywords from content")
        input_text = st.text_area("Enter your text here")

        if input_text is not None:
            if st.button("Extract Keywords"):
                # Display input text and extracted keywords
                col1, col2 = st.columns([1,1])
                with col1:
                    st.markdown("Your Input Text")
                    st.info(input_text)
                with col2:
                    st.markdown("Extracted Keywords")
                    result = model.extract_keywords(input_text, highlight=True) 
                    result = key_extract(result)
                    st.success(result)

    elif choice == "Keyword Extraction from Document":
        # File uploader for document
        st.subheader("Extract Keywords from Content")
        input_file = st.file_uploader("Upload your document here", type=['pdf'])

        if input_file is not None:
            if st.button("Extract Document"):
                # Save uploaded PDF file and extract text
                with open("doc_file.pdf", "wb") as f:
                    f.write(input_file.getbuffer())

                # Display uploaded file and extracted keywords
                col1, col2 = st.columns([1,1])
                with col1:
                    st.info("File uploaded successfully")
                    extracted_text = key_extract_from_pdf("doc_file.pdf")
                    st.markdown("Extracted Text is Below:")
                    st.info(extracted_text)
                with col2:
                    st.markdown("Extracted Keywords")
                    text = key_extract_from_pdf("doc_file.pdf")
                    result = model.extract_keywords(text, highlight=True) 
                    doc_translate = key_extract(result)
                    st.success(doc_translate)

app()
