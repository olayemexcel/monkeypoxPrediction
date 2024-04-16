#Libraries
import pandas as pd
import numpy as np
import streamlit as st

#Visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud
import plotly.graph_objs as go

import matplotlib
matplotlib.use('Agg')

#utils
import os
import joblib
import hashlib
# can also use passlib, bcrypt

# DB
from db_core import *
def generate_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def verify_hashes(password,hashes_text):
    if generate_hashes(password) == hashes_text:
        return hashes_text
    return False




def main():
    """Monkeypox Prediction Web App"""
    st.title("Monkeypox Prediction Visualization")

    menu = ["Home","Login","SignUp"]
    submenu = ["Plot","Prediction", "Metrics"]

    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Home":
        st.subheader("Home")
        st.text("What is Monkeypox?")

    elif choice == "Login":
        username = st.sidebar.text_input("username")
        password = st.sidebar.text_input("password", type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = generate_hashes(password)
            result = login_user(username,verify_hashes(password,hashed_pswd))

            if result:
                st.success("Welcome {}".format(username))

                activity = st.selectbox("Activity",submenu)
                if activity == "Plot":
                    st.subheader("Data Visualization")

                elif activity == "Prediction":
                    st.subheader("Predictive Analytics")
            
            else:
                st.warning("Incorrect Username/Password")


    elif choice == "SignUp":
        new_username = st.text_input("User name")
        new_password = st.text_input("Password", type='password')

        confirm_password = st.text_input("Confirm Password", type='password')
        if new_password == confirm_password:
            st.success("Password Confirmed")
        else:
            st.warning("Password not matched!")

        if st.button("Submit"):
            create_usertable()
            hashed_new_password = generate_hashes(new_password)
            add_userdata(new_username,hashed_new_password)
            st.success("You have successfully created a new account")
            st.info("Login to Get Started")



if __name__ == '__main__':
    main()