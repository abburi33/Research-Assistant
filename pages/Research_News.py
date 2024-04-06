import streamlit as st
import requests
import os
import json

# Load API key from environment variable
API_KEY = os.getenv("NEWS_API_KEY", "6eeababca09646489b00a8e5c093e65a")

def get_latest_research_from_top_journals(query, num_results=5):
    articles = []
    
    # List of top research journals
    journals = ["Nature", "Science", "The Lancet", "Cell", "Journal of the American Medical Association", 
                "New England Journal of Medicine", "Proceedings of the National Academy of Sciences", 
                "PLOS ONE", "Bioinformatics", "Journal of Biological Chemistry"]
    
    with st.spinner('Fetching latest research from top journals...'):
        for journal in journals:
            try:
                url = f"https://newsapi.org/v2/everything?q={query} {journal}&language=en&sortBy=publishedAt&pageSize={num_results}&apiKey={API_KEY}"
                response = requests.get(url)
                data = response.json()
                
                if data['status'] == 'ok':
                    articles.extend(data['articles'])
                
            except Exception as e:
                st.warning(f"Error fetching data from {journal}: {e}")
                
        articles = sorted(articles, key=lambda x: x['publishedAt'], reverse=True)[:num_results]
        
        if articles:
            for idx, article in enumerate(articles):
                st.markdown(f"#### {idx + 1}. [{article['title']}]({article['url']})", unsafe_allow_html=True)
                st.write(f"**Source:** {article['source']['name']}")
                st.write(f"**Published Date:** {article['publishedAt']}")
                st.write(f"**Description:** {article['description']}")
                
                # Save button for each article
                if st.button(f"Save Article {idx + 1}"):
                    save_article(article, idx)
                
                st.write('---')
            
        else:
            st.warning("No articles found.")

def save_article(article, idx):
    # Create a new directory to save articles if it doesn't exist
    if not os.path.exists('saved_articles'):
        os.makedirs('saved_articles')
    
    # Create a file with the article title and save the article content
    try:
        with open(f"saved_articles/{article['title']}.json", "w", encoding="utf-8") as file:
            json.dump(article, file, indent=4)
        
        st.success(f"Article {idx + 1} saved successfully!")
        
        # Provide a download link for the saved article
        download_link = f"[Download {article['title']}.json](saved_articles/{article['title']}.json)"
        st.markdown(download_link, unsafe_allow_html=True)
        
    except Exception as e:
        st.warning(f"Error saving article {article['title']}: {e}")

def main():
    st.title('Latest research from top journals...')

    # Literature Search Filters
    st.subheader('News Feed')

    with st.form("search_form"):
        query = st.text_input('Enter main search query:', 'Machine Learning')
        num_articles = st.text_input('Number of news articles:', '5')
        
        submitted = st.form_submit_button("Search")

    if submitted:
        get_latest_research_from_top_journals(query, int(num_articles))

if __name__ == "__main__":
    main()
