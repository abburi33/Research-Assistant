import streamlit as st
from langdetect import detect_langs
from PyPDF2 import PdfReader
import googletrans
from googletrans import Translator

st.set_page_config(layout="wide")

@st.cache_resource
def text_translate(text, maxlength=None):
    #create summary instance
    result = translator.translate(text)    
    return result

def translate_text_from_pdf(file_path):
    # Open the PDF file using PyPDF2
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        page = reader.pages[0]
        text = page.extract_text()
    return text

translator = Translator()    
choice = st.sidebar.selectbox("Select your choice", ["Translate Text", "Translate Document"])

if choice == "Translate Text":
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
    st.subheader("Translate your Document")
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
                text = translate_text_from_pdf("doc_file.pdf")
                doc_translate = text_translate(text)
                st.success(doc_translate)