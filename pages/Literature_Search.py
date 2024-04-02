import streamlit as st
from scholarly import scholarly

def search_scholar(query, year_filter=None, author_filter=None, journal_filter=None, num_results=5):
    search_query = scholarly.search_pubs(query)
    results = []
    for i in range(num_results):
        try:
            result = next(search_query)
            bib = result['bib']
            if (not year_filter or bib.get('pub_year') == year_filter) and \
               (not author_filter or author_filter.lower() in ', '.join(bib.get('author', ['']).lower())) and \
               (not journal_filter or journal_filter.lower() in bib.get('venue', '').lower()):
                results.append({
                    'Title': bib.get('title', ''),
                    'Author': ', '.join(bib.get('author', ['Unknown'])),
                    'Journal': bib.get('venue', ''),
                    'Year': bib.get('pub_year', ''),
                    'Abstract': bib.get('abstract', ''),
                    'Citations': result.get('num_citations', 0),
                    'URL': result.get('pub_url', '')
                })
        except StopIteration:
            break
    return results

st.title('Research Assistant for Literature Search and Management')

# Literature Search Filters
st.sidebar.title('Literature Search')
query = st.sidebar.text_input('Enter search query:', 'Machine Learning')
year_filter = st.sidebar.text_input('Filter by Year:', '')
author_filter = st.sidebar.text_input('Filter by Author:', '')
journal_filter = st.sidebar.text_input('Filter by Journal:', '')

if st.sidebar.button('Search'):
    results = search_scholar(query, year_filter, author_filter, journal_filter)
    st.write(f"### Search Results for '{query}'")
    for idx, result in enumerate(results, 1):
        st.write(f"#### {idx}. [{result['Title']}]({result['URL']})")
        st.write(f"**Authors:** {result['Author']}")
        st.write(f"**Journal:** {result['Journal']}")
        st.write(f"**Year:** {result['Year']}")
        st.write(f"**Abstract:** {result['Abstract']}")
        st.write(f"**Citations:** {result['Citations']}")
        st.write('---')
