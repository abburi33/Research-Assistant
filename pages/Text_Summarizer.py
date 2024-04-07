import streamlit as st
from txtai.pipeline import Summary
from PyPDF2 import PdfReader

st.set_page_config(layout="wide")

@st.cache_resource
def text_summary(text, maxlength=None):
    """
    Function to summarize text using the txtai library.

    Args:
    - text (str): The input text to be summarized.
    - maxlength (int, optional): Maximum length of the summary (default is None).

    Returns:
    - str: The summarized text.
    """
    # Create summary instance
    summary = Summary()
    result = summary(text, maxlength=maxlength)
    return result

def extract_text_from_pdf(file_path):
    """
    Function to extract text from a PDF file.

    Args:
    - file_path (str): The path to the PDF file.

    Returns:
    - str: The extracted text from the PDF.
    """
    # Open the PDF file using PyPDF2
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        page = reader.pages[0]
        text = page.extract_text()
    return text

def app():
    """
    Main function to run the Text Summarizer app.
    """
    st.title("TEXT SUMMARIZER")

    choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize Document"])

    if choice == "Summarize Text":
        st.subheader("Summarizing Your Text")
        input_text = st.text_area("Enter your text here")
        if input_text is not None:
            if st.button("Summarize Text"):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("*Your Input Text*")
                    st.info(input_text)
                with col2:
                    st.markdown("*Summary Result*")
                    result = text_summary(input_text)
                    st.success(result)

    elif choice == "Summarize Document":
        st.subheader("Summarizing Your Document")
        input_file = st.file_uploader("Upload your document here", type=['pdf'])
        if input_file is not None:
            if st.button("Summarize Document"):
                with open("doc_file.pdf", "wb") as f:
                    f.write(input_file.getbuffer())
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.info("File uploaded successfully")
                    extracted_text = extract_text_from_pdf("doc_file.pdf")
                    st.markdown("*Extracted Text is Below:*")
                    st.info(extracted_text)
                with col2:
                    st.markdown("*Summary Result*")
                    doc_summary = text_summary(extracted_text)
                    st.success(doc_summary)

if __name__ == "__main__":
    app()
