from secrets import choice
from turtle import shape
from matplotlib.pyplot import axis, title
from numpy import place
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import pickle
import requests

st.set_page_config(layout="wide")
styl = f"""
    <style>
        img{{
            height : 240px;
            margin : 8px;   
            border-radius: 5%;
        }}
        
    </style>
    """
st.markdown(styl, unsafe_allow_html=True)
placeholder = st.empty()
try:
    user_df = pd.read_csv('Users.csv')
    print("i ran")
except Exception:
    user_df = pd.DataFrame({'usernames': ['dpatel', 'dvyas'],
                            'User-id': [672, 673], 'Password': [123, 123]
                            })
    user_df.to_csv('Users.csv', index=False)
user_password_map = {}
for username, passwd in zip(user_df["usernames"], user_df["Password"]):
    user_password_map[username] = str(passwd)
user_id_map = {}
for username, user_id in zip(user_df["usernames"], user_df["User-id"]):
    user_id_map[username] = str(user_id)
tmdb_mov_map = pickle.load(open('tmdb_mov_map.pkl', 'rb'))
title_mov_map = pickle.load(open('title_mov_map.pkl', 'rb'))
# users_dict = pickle.load(open('watched1.pkl', 'rb'))
# users_map={671:'dpatel', 672:'dvyas'}

# names = ['Devasy Patel', 'Dhruvil Vyas']
# usernames = ['dpatel', 'dvyas']
# passwords = ['123', '123']
# hashed_passwords = stauth.Hasher(passwords).generate()
# authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
#     'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)
# name, authentication_status, username = authenticator.login('Login', 'main')
# if authentication_status:
#     authenticator.logout('Logout', 'main')
#     st.write('Welcome *%s*' % (name))
#     st.title('Some content')
# elif authentication_status == False:
#     st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')


def main():
    placeholder1 = st.empty()
    if 'key' not in st.session_state:
        st.session_state['key'] = ""
    if(st.session_state['key'] == ""):
        with placeholder1.container():
            st.title("Login/Signup")
            menu = ["Home", "Login", "Signup"]
            choice = st.sidebar.selectbox("Menu", menu)

            if choice == "Home":
                st.subheader("Home")
            elif choice == "Login":
                st.subheader("Login Section")
                username = st.text_input("User name")
                password = st.text_input("Password", type="password")
                # st.sidebar.button("Login")
                if st.button("Login"):
                    # user_df.loc[user_df['usernames'] == username]
                    if(username in user_password_map):
                        # means user is present

                        if user_password_map[username] == password:
                            placeholder1.empty()
                            with placeholder.container():
                                st.session_state['key'] = username
                            # task = st.selectbox("Task")
                        else:
                            # st.write(passw, type(password), username)
                            st.warning("Incorrect Username/Password")

                    else:
                        st.warning("Incorrect Username/Password")

            elif choice == "Signup":
                st.subheader("Signup Section")
                new_user = st.text_input("Username")
                if new_user not in user_password_map:
                    new_password = st.text_input("Password", type='password')
                    if st.button("Signup"):
                        rows = user_df.shape[0]
                        user_df.loc[len(user_df.index)] = [
                            new_user, 672+rows, new_password]
                        st.success("You Have Signed Sucessfully")
                        st.info("Go to login menu to login")
                        user_df.to_csv('Users.csv', index=False)
                else:
                    st.warning("Username alreay exists")
    if(st.session_state['key'] != ""):
        username = st.session_state['key']
        with placeholder1.container():
            # P = "E:\\College\\New folder (2)\\MR_Project\\"
            P = ""
            username = st.session_state['key']
            st.success("Logged In as {}".format(username))
            st.title('Movie recommendation system')

            l = []
            # l_dict = {}

            def movies_csv2dict(string):
                # f = open(string, "r+")
                l_dict = {}
                # f.readline()
                movies = pd.read_csv(string)
                # for l in f.readlines():
                for i in range(movies.shape[0]):
                    l_dict[movies.iloc[i, 1]] = movies.iloc[i, 0]
                return l_dict

            # recmovi = set({})
            mapped_movies = movies_csv2dict(
                P + "userbased/movies.csv")  # name : id
            # st.write(mapped_movies)
            # with pickle
            # with open("users.csv", "r+") as f:
            #     file = f.readlines()
            #     recmovi = set(file)
            #     pass

            def csv2dict(string):
                f = open(string, "r+")
                l_dict = {}
                f.readline()
                df = pd.read_csv(string)

                rows = df.shape[0]
                # print(mapped_movies)
                for i in range(rows):
                    user_id, movie_id, rating = df.iloc[i,
                                                        0], df.iloc[i, 1], df.iloc[i, 1]
                # for l in f.readlines():
                #     user_id, movie_id, rating, _ = l.split(",")
                #     # movie_id = mapped_movies[movie]
                    if int(user_id) not in l_dict:
                        l_dict[int(user_id)] = {}
                        l_dict[int(user_id)][int(movie_id)] = float(rating)
                    else:
                        l_dict[int(user_id)][int(movie_id)] = float(rating)
                return l_dict

            def dict2csv(string, dict):
                u, m, r = [], [], []
                for user_id in dict:
                    for movie_id in dict[user_id]:
                        u.append(user_id)
                        m.append(movie_id)
                        r.append(dict[user_id][movie_id])
                dict = {
                    'user_id': u, 'movie_id': m, 'ratings': r
                }
                df = pd.DataFrame(dict)
                df.to_csv(string, index=False, header=False)
            try:

                # recmovi = pickle.load(open('pick.pkl', 'rb'))
                watched_movies = pickle.load(
                    open(P + 'userbased/watched1.pkl', 'rb'))
                dict2csv("ratings_modified.csv", watched_movies)
                # watched_movies = csv2dict('userbased/ratings.csv')
            except Exception as e:
                st.write("No pickle file found", e)
                # watched_movies = {672 : {'Jumanji (1995)': 4}}
                # watched_movies = csv2dict('/home/dhruvil/MR_Project/userbased/ratings.csv')

                print("hello")

            try:
                movies = pd.read_csv(P + 'userbased/movies.csv')
            except Exception as e:
                print("hello sorry i found an exrror", e)
            st.title("Provide your watched movies")
            user_id = user_id_map[username]
            option = st.selectbox('Enter Movie Name', (movies['title']))
            rating = st.slider('Enter Rating', 1, 5)
            emoji = "⭐"
            st.markdown("<p style='text-align: center;'>" + emoji *
                        rating + "</p>", unsafe_allow_html=True)
            result = st.button("Add to watched")
            if result:
                # print(type(watched_movies))
                user_id = int(user_id)
                if user_id not in watched_movies:
                    watched_movies[int(user_id)] = {int(mapped_movies[option]): rating}
                    st.write("You have rated {} {} stars".format(option, rating))
                # print("watched movies is here", watched_movies)
                else:
                    if int(mapped_movies[option]) in watched_movies[user_id]:
                        st.write("User id is here: ", user_id)
                        st.write("Rating is updated. You have earlier rated {} {} stars".format(
                            option, watched_movies[user_id][int(mapped_movies[option])]))
                    else:

                        st.write("Movie added")
                    watched_movies[user_id][int(mapped_movies[option])] = rating
                    # pickle.dump(recmovi, open('pick.pkl', 'wb'))
                pickle.dump(watched_movies, open(
                    P + 'userbased/watched1.pkl', 'wb'))
            core_matrix = pickle.load(
                open(P + 'userbased/corrMatrix.pkl', 'rb'))

            def get_similar(movie_name, rating):
                similar_ratings = core_matrix[movie_name]*(rating-2.5)
                similar_ratings = similar_ratings.sort_values(ascending=False)
                # print(type(similar_ratings))
                return similar_ratings
            
            user_id = int(user_id)
            if(user_id in watched_movies):
                user_dict = watched_movies[user_id]
                similar_movies = pd.DataFrame()
                # print("Title mov map is here: ", title_mov_map)
                def fetch_poster(dict):
                    for movie, id in dict.items():
                        response = requests.get(
                        f"https://api.themoviedb.org/3/movie/{id}?api_key=5f22100b0a8f34d1ea15eb5605bc2d87&language=en-US")
                        response = response.json()

                        data = response["poster_path"]
                        poster = f"https://image.tmdb.org/t/p/w500/{data}"
                        dict[movie] = poster
                    return dict

                def display_from_dict(dict, message):
                    l = dict2dlist(dict)
                    img = []
                    caption = []
                    for i in range(len(l)):

                        img.append(l[i][0])
                        caption.append(l[i][1])
                    # st.columns here since it is out of beta at the time I'm writing this
                    # cols = cycle(st.columns(4))
                    # for idx, filteredImage in enumerate(img):
                    #     next(cols).image(filteredImage, width=150,
                    #                      caption=caption[idx], use_column_width=False)
                    st.write(message)
                    st.image(img, width=155, caption=caption, use_column_width= False)

                def dict2dlist(dict):
                    l = []
                    for x, y in dict.items():
                        temp = [y, x]
                        l.append(temp)
                    return l



                for movie, rating in user_dict.items():
                    moviename = title_mov_map[int(movie)]

                    similar_movies = similar_movies.append(
                        get_similar(moviename, rating), ignore_index=True)
                similar_movies.head(10)
                x = []
                print(similar_movies.sum().head(20))
                for y in similar_movies.sum().sort_values(ascending=False).head(20).index:
                    if y not in user_dict:
                        x.append(y)
                st.write("Suggested movies are: ", x)
                title_tmdb ={}
                for i in x:
                    title_tmdb[i] = tmdb_mov_map[mapped_movies[i]]   #(tmdb_mov_map[i])
                display_from_dict(fetch_poster(title_tmdb), "Your suggestions")

            # {user_id : {movie_id : rating}}


if __name__ == '__main__':
    main()
