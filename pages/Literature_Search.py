import streamlit as st
from scholarly import scholarly

def search_scholar(query, num_results=5):
    search_query = scholarly.search_pubs(query)
    results = []
    for i in range(num_results):
        try:
            result = next(search_query)
            bib = result['bib']
            results.append({
                'Title': bib.get('title', ''),
                'Author': ', '.join(bib.get('author', ['Unknown'])),
                'Journal': bib.get('venue', ''),
                'Year': bib.get('pub_year', ''),
                'URL': result.get('pub_url', '')
            })
        except StopIteration:
            break
    return results

st.title('Research Assistant for Literature Search and Management')

# Literature Search
st.sidebar.title('Literature Search')
query = st.sidebar.text_input('Enter search query:', 'Machine Learning')

if st.sidebar.button('Search'):
    results = search_scholar(query)
    st.write(f"### Search Results for '{query}'")
    for idx, result in enumerate(results, 1):
        st.write(f"#### {idx}. [{result['Title']}]({result['URL']})")
        st.write(f"**Authors:** {result['Author']}")
        st.write(f"**Journal:** {result['Journal']}")
        st.write(f"**Year:** {result['Year']}")
        st.write('---')
