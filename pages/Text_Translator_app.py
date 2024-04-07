import streamlit as st
from PyPDF2 import PdfReader
from googletrans import Translator

# Set page layout to wide
st.set_page_config(layout="wide")

# Function to translate text to the desired language
@st.cache_resource
def text_translate(text, maxlength=None):
    """
    Function to translate text to the desired language.

    Args:
    - text (str): The text to be translated.
    - maxlength (int, optional): Maximum length of the translated text. Defaults to None.

    Returns:
    - str: The translated text.
    """
    # Create translator instance
    translator = Translator()
    # Translate the text
    result = translator.translate(text)
    return result.text

# Function to extract text from a PDF file and translate it
def translate_text_from_pdf(file_path):
    """
    Function to extract text from a PDF file and translate it.

    Args:
    - file_path (str): Path to the PDF file.

    Returns:
    - str: The translated text extracted from the PDF.
    """
    # Open the PDF file using PyPDF2
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        page = reader.pages[0]
        text = page.extract_text()
    # Translate the extracted text
    translated_text = text_translate(text)
    return translated_text

# Main function to run the translation app
def main():
    """
    Main function to run the translation app.
    """
    # Set app title
    st.title("TEXT TRANSLATOR")

    # Sidebar to select translation option
    choice = st.sidebar.selectbox("Select your choice", ["Translate Text", "Translate Document"])

    if choice == "Translate Text":
        # Translate text option
        st.subheader("Translate Your Text Content")
        input_text = st.text_area("Enter your text here")
        if input_text is not None:
            if st.button("Translate Text"):
                col1, col2 = st.columns([1,1])
                with col1:
                    st.markdown("Your Input Text")
                    st.info(input_text)
                with col2:
                    st.markdown("Translated Result")
                    result = text_translate(input_text)
                    st.success(result)

    elif choice == "Translate Document":
        # Translate document option
        st.subheader("Translate Your Document")
        input_file = st.file_uploader("Upload your document here", type=['pdf'])
        if input_file is not None:
            if st.button("Translate Document"):
                with open("doc_file.pdf", "wb") as f:
                    f.write(input_file.getbuffer())
                col1, col2 = st.columns([1,1])
                with col1:
                    st.info("File uploaded successfully")
                    extracted_text = translate_text_from_pdf("doc_file.pdf")
                    st.markdown("Extracted Text is Below:")
                    st.info(extracted_text)
                with col2:
                    st.markdown("Translated Result")
                    translated_text = translate_text_from_pdf("doc_file.pdf")
                    st.success(translated_text)

if __name__ == "__main__":
    main()
