import streamlit as st
import requests

# Define the API key for News API
API_KEY = "6eeababca09646489b00a8e5c093e65a"

def main():
    """
    Main function to run the Research Assistant Streamlit app.
    """
    # Header
    st.title('Research Assistant')
    st.write("<span style='font-size:18px;'>'Your one-stop solution for literature search, meeting scheduling, to-do lists, feedback collection, and latest research developments.</span>'", unsafe_allow_html=True)

    # Displaying latest research news
    st.header("Latest Research Developments")
    display_latest_research_news()

def display_latest_research_news():
    """
    Function to fetch and display the latest research news.
    """
    # Fetching news data from News API
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Check if 'articles' key exists in the response
    if 'articles' in data:
        articles = data['articles']
        # Display articles
        for article in articles[:5]:  # Displaying the first 5 recent articles
            title = article.get('title', 'No Title Available')
            published_at = article.get('publishedAt', 'No Date Available')
            description = article.get('description', 'No Description Available')
            url = article.get('url', '#')
            
            st.markdown(f"**{title}**", unsafe_allow_html=True)
            st.write(f"*Published Date:* {published_at}")
            st.write(f"*Description:* {description}")
            st.write(f"[Read more]({url})")
            st.write('---')
    else:
        # Display a warning if no recent research news found
        st.warning("No recent research news found.")
        print("No articles found")

# Run the main function
if __name__ == "__main__":
    main()
