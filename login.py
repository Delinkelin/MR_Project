import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import pickle


users_dict = pickle.load(open('watched1.pkl', 'rb'))
users_map={671:'dpatel', 672:'dvyas'}

names = ['Devasy Patel', 'Dhruvil Vyas']
usernames = ['dpatel', 'dvyas']
passwords = ['123', '123']
hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write('Welcome *%s*' % (name))
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')