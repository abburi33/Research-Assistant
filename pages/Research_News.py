import streamlit as st
import requests

def search_scopus(query, api_key, subtopic=None, year_filter=None, num_results=5):
    """
    Function to search for articles on Scopus based on the provided query and filters.
    
    Args:
    - query (str): The main search query.
    - api_key (str): The API key for accessing the Scopus API.
    - subtopic (str): The subtopic to narrow down the search (optional).
    - year_filter (str): The year filter to limit search results (optional).
    - num_results (int): The number of articles to retrieve (default is 5).
    
    Returns:
    - List[dict]: A list of dictionaries containing information about the search results.
    """
    url = "https://api.elsevier.com/content/search/scopus"
    headers = {
        "X-ELS-APIKey": api_key
    }
    params = {
        "query": query,
        "count": num_results
    }
    if subtopic:
        params["subtopic"] = subtopic
    if year_filter:
        params["date"] = year_filter  # Corrected parameter for year filter
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data.get("search-results", {}).get("entry", [])

def app():
    """
    Main function to run the Research Assistant for literature search.
    """
    st.title('RESEARCH ASSISTANT FOR LITERATE SEARCH')

    # Literature Search Filters
    st.sidebar.title('Literature Search')

    with st.sidebar.form("search_form"):
        query = st.text_input('Enter main search query:', 'Machine Learning')
        subtopic = st.text_input('Enter subtopic:', '')
        year_filter = st.text_input('Filter by Year (YYYY):', '')
        num_articles = st.text_input('Enter number of articles:', '3')
        
        submitted = st.form_submit_button("Search")

    if submitted:
        api_key = "19fb6dbf6b205c5d5c84c1543af87a7f"
        results = search_scopus(query, api_key, subtopic, year_filter, int(num_articles))
        
        for idx, result in enumerate(results, start=1):
            article_title = result.get('dc:title', '')
            article_link = result.get('prism:url', '')
            st.write(f"#### {idx}. [{article_title}]({article_link})")
            st.write(f"Authors: {', '.join(result.get('dc:creator', ['Unknown']))}")
            st.write(f"Journal: {result.get('prism:publicationName', '')}")
            st.write(f"Year: {result.get('prism:coverDate', '')}")
            abstract = result.get('dc:description', '')
            st.write(f"Abstract: {abstract}" if abstract else "Abstract: Not available")
            st.write(f"Citations: {result.get('citedby-count', '')}")
            st.write('---')

if __name__ == "__main__":
    app()
