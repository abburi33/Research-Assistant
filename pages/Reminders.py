import streamlit as st
import requests
import time
import os
import shutil

def get_latest_research_from_top_journals(query, num_results=5):
    articles = []
    
    # List of top research journals
    journals = ["Nature", "Science", "The Lancet", "Cell", "Journal of the American Medical Association", "New England Journal of Medicine", "Proceedings of the National Academy of Sciences", "PLOS ONE", "Bioinformatics", "Journal of Biological Chemistry"]
    
    with st.spinner('Fetching latest research from top journals...'):
        try:
            for journal in journals:
                url = f"https://newsapi.org/v2/everything?q={query} {journal}&language=en&sortBy=publishedAt&pageSize={num_results}&apiKey=YOUR_NEWSAPI_KEY"
                response = requests.get(url)
                data = response.json()
                
                if data['status'] == 'ok':
                    articles.extend(data['articles'])
                
            articles = sorted(articles, key=lambda x: x['publishedAt'], reverse=True)[:num_results]
            
            if articles:
                for idx, article in enumerate(articles):
                    st.markdown(f"#### {idx + 1}. [{article['title']}]({article['url']})", unsafe_allow_html=True)
                    st.write(f"**Source:** {article['source']['name']}")
                    st.write(f"**Published Date:** {article['publishedAt']}")
                    st.write(f"**Description:** {article['description']}")
                    
                    # Save button for each article
                    if st.button(f"Save Article {idx + 1}"):
                        save_article(article)
                    
                    st.write('---')
            
            else:
                st.warning("No articles found.")
                
        except Exception as e:
            st.warning(f"Error fetching data: {e}")

def save_article(article):
    # Create a new directory to save articles if it doesn't exist
    if not os.path.exists('saved_articles'):
        os.makedirs('saved_articles')
    
    # Create a file with the article title and save the article content
    with open(f"saved_articles/{article['title']}.txt", "w", encoding="utf-8") as file:
        file.write(f"Title: {article['title']}\n")
        file.write(f"Source: {article['source']['name']}\n")
        file.write(f"Published Date: {article['publishedAt']}\n")
        file.write(f"Description: {article['description']}\n")
        file.write(f"URL: {article['url']}\n")
        file.write(f"Content: {article['content']}\n")

def main():
    st.title('Research Assistant for Literature Search and Management')

    # Literature Search Filters
    st.sidebar.title('Literature Search')

    with st.sidebar.form("search_form"):
        query = st.text_input('Enter main search query:', 'Machine Learning')
        num_articles = st.text_input('Enter number of articles:', '5')
        
        submitted = st.form_submit_button("Search")

    if submitted:
        get_latest_research_from_top_journals(query, int(num_articles))

if __name__ == "__main__":
    main()
