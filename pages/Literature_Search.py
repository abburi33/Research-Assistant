import subprocess
import webbrowser
import streamlit as st
from scholarly import scholarly
import time
import os

def search_scholar(query, num_results=5, timeout=60):
    """
    Function to search for scholarly articles using the given query.

    Args:
        query (str): The main search query.
        num_results (int, optional): Number of articles to fetch. Defaults to 5.
        timeout (int, optional): Timeout duration for the search. Defaults to 60.

    Returns:
        list: List of dictionaries containing information about the fetched articles.
    """
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

def main():
    """
    Main function to run the Research Assistant for Literature Search app.
    """
    st.title('Research Assistant for Literature Search')
    
    if st.button('Chatbot'):
        # django_app_url = "http://3.96.64.144:8000"
        django_app_url = "http://localhost:8000"

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define the path to the manage.py file in your Django project
        manage_py_path = os.path.join(script_dir, "django_chatbot", "manage.py")
        
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
        results = search_scholar(query, int(num_articles))

if __name__ == "__main__":
    main()
