import streamlit as st
import pickle
import numpy as np
from streamlit_option_menu import option_menu

final_rating = pickle.load(open('models/final_rating.pkl','rb'))
book_pivot = pickle.load(open('models/book_pivot.pkl','rb'))
books = pickle.load(open('models/books.pkl','rb'))
similarity_scores = pickle.load(open('models/similarity_scores.pkl','rb'))

def main():

    st.set_page_config(
        page_title="Book Recommender",
        page_icon="book",
        layout="wide",
    )
    
    with st.sidebar:
        selected = option_menu("Modes", ["Home",'Recommender'], 
            icons=['house', 'book'], menu_icon="cast", default_index = 0)
        selected
    
    if selected == 'Home' :
        st.title(":blue[BOOK RECOMMENDATION PREDICTOR] :book:")
        content_html = """"""
        st.write(content_html)
        html_temp_home1 = """<div style="padding:10px">
                                <h2 style="color:sky">Top Books</h2>                 
                                </div>
                                </br>"""
        st.markdown(html_temp_home1, unsafe_allow_html=True)
        
        # st.write('### Top Books')
        for title, author, img_url, votes in zip(
            final_rating['title'].values, 
            final_rating['author'].values, 
            final_rating['img_url_m'].values, 
            final_rating['no_of_rating'].values
        ):
            st.image(img_url, width=100)
            st.write(f'**{title}** by {author}')
            st.write(f'Votes: {votes}')
            st.write('---')

    # Recommender page
    if selected == 'Recommender' :
        
        user_input = st.text_input('Enter a book title')
        if user_input:
            try:
                index = np.where(book_pivot.index == user_input)[0][0]
                similar_items = sorted(
                    list(enumerate(similarity_scores[index])), 
                    key=lambda x: x[1], 
                    reverse=True
                )[1:5]

                st.write('### Recommended Books')
                for i in similar_items:
                    temp_df = books[books['title'] == book_pivot.index[i[0]]]
                    title = temp_df['title'].values[0]
                    author = temp_df['author'].values[0]
                    img_url = temp_df['img_url_m'].values[0]
                    st.image(img_url, width=100)
                    st.write(f'**{title}** by {author}')
                    st.write('---')
            except IndexError:
                st.write('Book not found. Please check the title and try again.')

if __name__ == "__main__":
    main()
