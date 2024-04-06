import streamlit as st
import requests
import os
import subprocess
import webbrowser
from scholarly import scholarly
import time
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
        
        return articles

def search_scholar(query, num_results=5, timeout=60):
    results = []
    progress_bar = st.empty()
    seen_titles = set()
    
    start_time = time.time()
    
    with st.spinner('Searching for articles...'):
        while time.time() - start_time < timeout and len(results) < num_results:
            try:
                search_query = scholarly.search_pubs(query)
                
                for i in range(5):  # Fetching 5 articles at a time
                    result = next(search_query, None)
                    
                    if result is None:
                        break
                    
                    bib = result['bib']
                    title = bib.get('title', '')
                    
                    if title not in seen_titles:
                        seen_titles.add(title)
                        
                        results.append({
                            'Title': title,
                            'Author': ', '.join(bib.get('author', ['Unknown'])),
                            'Journal': bib.get('venue', ''),
                            'Year': bib.get('pub_year', ''),
                            'Abstract': bib.get('abstract', ''),
                            'Citations': result.get('num_citations', 0),
                            'URL': result.get('pub_url', '')
                        })
                        
                        st.markdown(f"#### {len(results)}. [{title}]({result.get('pub_url', '')})", unsafe_allow_html=True)
                        st.write(f"**Authors:** {', '.join(bib.get('author', ['Unknown']))}")
                        st.write(f"**Journal:** {bib.get('venue', '')}")
                        st.write(f"**Year:** {bib.get('pub_year', '')}")
                        st.write(f"**Abstract:** {bib.get('abstract', '')}")
                        st.write(f"**Citations:** {result.get('num_citations', 0)}")
                        st.write('---')
                        
                        progress_bar.progress(len(results) / num_results)
                        
                        if len(results) >= num_results:
                            break
                    
                if len(results) >= num_results:
                    break
                
            except Exception as e:
                st.warning(f"Error fetching data. Retrying...")
                time.sleep(2)  # Add a delay of 2 seconds between retry attempts
    
    progress_bar.empty()
    return results[:num_results]  # Return only the required number of articles

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
    st.title('Research Assistant for Literature Search')
    
    if st.button('Chatbot'):
        django_app_url = "http://localhost:8000"

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define the path to the manage.py file in your Django project
        manage_py_path = os.path.join(script_dir, "django_chatbot", "manage.py")
        print(manage_py_path)
        
        # Define the command to run your Django app
        django_command = f"python {manage_py_path} runserver"
        
        # Run the Django app using subprocess
        subprocess.Popen(django_command, shell=True)
        webbrowser.open_new_tab(django_app_url)

    # Literature Search Filters
    st.subheader('Literature Search')

    with st.form("search_form"):
        query = st.text_input('Enter main search query:', 'Machine Learning')
        num_articles = st.text_input('Enter number of articles:', '5')
        
        submitted = st.form_submit_button("Search")

    if submitted:
        scholarly_articles = search_scholar(query, int(num_articles))
        if scholarly_articles:
            for article in scholarly_articles:
                st.markdown(f"#### [{article['title']}]({article['url']})", unsafe_allow_html=True)
                st.write(f"**Source:** {article['source']['name']}")
                st.write(f"**Published Date:** {article['publishedAt']}")
                st.write(f"**Description:** {article['description']}")
                
                # Save button for each article
                if st.button(f"Save Article: {article['title']}"):
                    save_article(article, scholarly_articles.index(article) + 1)
                
                st.write('---')
        else:
            web_articles = get_latest_research_from_top_journals(query, int(num_articles))
            if web_articles:
                for idx, article in enumerate(web_articles):
                    st.markdown(f"#### {idx + 1}. [{article['title']}]({article['url']})", unsafe_allow_html=True)
                    st.write(f"**Source:** {article['source']['name']}")
                    st.write(f"**Published Date:** {article['publishedAt']}")
                    st.write(f"**Description:** {article['description']}")
                    
                    # Save button for each article
                    if st.button(f"Save Article: {article['title']}"):
                        save_article(article, idx + 1)
                    
                    st.write('---')
            else:
                st.warning("No articles found.")

if __name__ == "__main__":
    main()
