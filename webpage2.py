import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud
import plotly.graph_objs as go
import hashlib


import matplotlib
matplotlib.use('Agg')

#utils
import os
import joblib
import hashlib

# import functions from set up db_core.py 
from db_core import create_usertable, add_userdata, login_user

def generate_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def verify_hashes(password, hashed_text):
    return generate_hashes(password) == hashed_text

def create_sidebar_menu():
    st.sidebar.title("Monkeypox ML Visualization")
    menu_selection = st.sidebar.radio("Menu", ["Home", "Data Visualization", "Model Evaluation", "About"])
    return menu_selection

def display_home_page():
    st.title("Welcome to Monkeypox ML Visualization")
    st.image("image/im1.jpg", use_column_width=True)
    st.write("This web application provides visualization of Monkeypox prediction using machine learning models.")


# Dataset Visualization Section
def display_data_visualization():
    st.title("Data Visualization")
    st.write("Here you can explore visualizations of Monkeypox data.")
    # Load data and show
    df = pd.read_csv("first_cleaned_dataset.csv") 
    st.write(df.head())

    # Display dataset information
    st.subheader("Dataset Information")
    st.write("Shape of the dataset:")
    st.write(df.shape)
    st.write("Basic information about the dataset:")
    st.write("This dataset contains dated records of carefully selected and organized Monkeypox cases from the 2022 outbreak.")
    st.write("Descriptive statistics of the dataset:")
    st.write(df.describe())

    # Dropdown menu to select cases plot
    plot_option = st.selectbox("Select Plot", ["Distribution of Cases per Country", "Reported Cases: Top Countries Affected",
                                               "Confirm Cases Distribution","Countries per case distribution","Most Common Symptoms/Signs",
                                               "Cases Distribution over Time","Day of the week with highest confirmation",
                                               "Age Group Mostly Affected","Cases by Gender"])

    # Plot distribution of cases per country
    if plot_option == "Distribution of Cases per Country":
        country_cases = df.groupby('Country')['Status'].count().reset_index()
        country_cases.columns = ['Country', 'Cases']
        
        st.subheader("Distribution of Cases per Country")
        fig = px.bar(country_cases, x='Country', y='Cases', title="Distribution of Cases per Country")
        fig.update_layout(xaxis_title="Country", yaxis_title="Number of Cases")
        st.plotly_chart(fig)

    # Plot reported cases for top countries affected
    elif plot_option == "Reported Cases: Top Countries Affected":
        top_countries_cases = df.groupby('Country')['Status'].count().nlargest(n=10).reset_index()
        
        st.subheader("Reported Cases: Top Countries Affected")
        fig = px.bar(top_countries_cases, x='Country', y='Status', color='Country')
        fig.update_layout(xaxis_tickangle=-45, bargap=0.2, height=600, width=1000)  # Rotate x-axis labels, increase width, and set height
        st.plotly_chart(fig)
    # Plot Confirm cases distribution
    elif plot_option == "Confirm Cases Distribution":
        st.subheader("Confirm Cases Distribution")
        sns.set_style("whitegrid")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x='Status', data=df, ax=ax)
        plt.xlabel("Status")
        plt.ylabel("Number of Cases")
        plt.title("Distribution of Confirm Cases")
        st.pyplot(fig) 
    # Plot Countries per case distribution
    elif plot_option == "Countries per case distribution":
        # Top cases by county in the descending order
        top_affected_countries = list(df['Country'].value_counts().to_frame().nlargest(10,'Country')['Country'].index)
        #Countries per case distribution
        top_countries = df[df['Country'].isin(top_affected_countries)]
        st.subheader("Countries per case distribution")
        fig = px.histogram(top_countries, x='Country', color='Status')
        fig.update_layout(xaxis_title="Country", yaxis_title="Count", xaxis_tickangle=-45)
        st.plotly_chart(fig)
        # Plot WordCloud for most common symptoms/signs
    elif plot_option == "Most Common Symptoms/Signs":
        st.subheader("Most Common Symptoms/Signs")
        
        # Prepare the text data
        text_data = ' '.join(df['Symptoms'].fillna('0').tolist())
        
        # Generate WordCloud
        wordcloud = WordCloud().generate(text_data)
        
        # Plot WordCloud
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)
         # Plot Cases Distribution over Time
    elif plot_option == "Cases Distribution over Time":
        st.subheader("Cases Distribution over Time")
        
        # Convert Date_confirmation to DateTime
        df['Date_confirmation'] = pd.to_datetime(df['Date_confirmation'])
        
        # Group data by date without time
        date_distribution = df.groupby(df['Date_confirmation'].dt.date)['Status'].size()
        
        # Visualize distribution per date/Number of cases per day based on data confirmation was made
        plt.figure(figsize=(10, 6))
        date_distribution.plot(kind='bar')
        plt.xlabel("Date Confirmation")
        plt.ylabel("Number of Cases")
        plt.title("Cases Distribution over Time")
        st.pyplot(plt)
        # Plot Day/Weekend/Week Distribution
    elif plot_option == "Day of the week with highest confirmation":
        st.subheader("Day of the week with highest confirmation")
        
        # Convert Date_confirmation to DateTime
        df['Date_confirmation'] = pd.to_datetime(df['Date_confirmation'])
        
        # Extract day of the week
        df['Day_of_week'] = df['Date_confirmation'].dt.day_name()
        
        # Count the occurrences of each day
        day_counts = df['Day_of_week'].value_counts()
        
        # Create interactive bar plot
        fig = px.bar(day_counts, x=day_counts.index, y=day_counts.values, labels={'x':'Day of the Week', 'y':'Number of Cases'}, 
                    title='Day/Weekend/Week Distribution', color=day_counts.values)
        fig.update_traces(marker_color='skyblue', marker_line_color='rgb(8,48,107)', 
                        marker_line_width=1.5, opacity=0.6)
        fig.update_layout(showlegend=False)
        
        # Show plot
        st.plotly_chart(fig)
        # Plot Age Group Mostly Affected
    elif plot_option == "Age Group Mostly Affected":
        st.subheader("Age Group Mostly Affected")

        # Calculate the count of cases for each age group
        age_affect = df['Age'].dropna().value_counts().sort_index()
        
        # Select the top 10 age groups
        top_10_age_groups = age_affect[:10]
        
        # Create a DataFrame for the top 10 age groups
        age_group_data = pd.DataFrame({
            'Age Group': top_10_age_groups.index,
            'Count': top_10_age_groups.values
        })
        
        # Create an interactive bar plot
        fig = px.bar(age_group_data, x='Age Group', y='Count', title='Age Group Mostly Affected',
                    labels={'Count': 'Number of Cases'},
                    color='Count', color_continuous_scale='Viridis')

        # Add text annotations on the bars
        fig.update_traces(text=top_10_age_groups.values, textposition='outside')

        # Update layout for better appearance
        fig.update_layout(
            xaxis=dict(tickangle=45),
            showlegend=False,
            autosize=False,
            width=800,
            height=500
        )

        # Show the plot
        st.plotly_chart(fig)
        # Plot Cases by Gender
    elif plot_option == "Cases by Gender":
        st.subheader("Cases by Gender")

        # Check Gender distribution
        gender_counts = df['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']

        # Create an interactive pie chart
        fig = px.pie(gender_counts, names='Gender', values='Count', title='Gender Distribution', 
                    hover_data=['Gender', 'Count'], labels={'Gender': 'Gender Distribution'})

        # Adjust layout for better readability
        fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.1 if i == gender_counts['Gender'].iloc[0] else 0 for i in gender_counts['Gender']])
        fig.update_layout(legend=dict(title='Gender'))

        # Show the interactive plot
        st.plotly_chart(fig)
                



# Model Evaluation Section
def display_model_evaluation():
    st.title("Model Evaluation")
    st.write("Performance metrics of machine learning models for Monkeypox prediction.")

    # Load the evaluation metrics for each model
    evaluation_metrics = {
        'Random Forest': {'Accuracy': 96.04, 'Precision': 96.31, 'Recall': 96.04, 'F1-score': 96.13, 'AUC-ROC': 99.27},
        'XGBoost': {'Accuracy': 92.95, 'Precision': 93.63, 'Recall': 92.95, 'F1-score': 93.21, 'AUC-ROC': 98.53},
        'Decision Tree': {'Accuracy': 94.27, 'Precision': 95.29, 'Recall': 94.27, 'F1-score': 94.66, 'AUC-ROC': 97.63}
    }

    # Convert the evaluation metrics into a DataFrame
    df_metrics = pd.DataFrame(evaluation_metrics).T

    # Load the evaluation metrics for each model
    evaluation_metrics = {
        'Random Forest': {'Accuracy': 96.04, 'Precision': 96.31, 'Recall': 96.04, 'F1-score': 96.13, 'AUC-ROC': 99.27},
        'XGBoost': {'Accuracy': 92.95, 'Precision': 93.63, 'Recall': 92.95, 'F1-score': 93.21, 'AUC-ROC': 98.53},
        'Decision Tree': {'Accuracy': 94.27, 'Precision': 95.29, 'Recall': 94.27, 'F1-score': 94.66, 'AUC-ROC': 97.63}
    }

    # Convert the evaluation metrics into a DataFrame
    df_metrics = pd.DataFrame(evaluation_metrics).T

    # Plot evaluation metrics using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Accuracy', x=df_metrics.index, y=df_metrics['Accuracy']),
        go.Bar(name='Precision', x=df_metrics.index, y=df_metrics['Precision']),
        go.Bar(name='Recall', x=df_metrics.index, y=df_metrics['Recall']),
        go.Bar(name='F1-score', x=df_metrics.index, y=df_metrics['F1-score']),
        go.Bar(name='AUC-ROC', x=df_metrics.index, y=df_metrics['AUC-ROC'])
    ])

    # Update the layout of the plot
    fig.update_layout(barmode='group', title='Model Evaluation Metrics', xaxis_title='Model', yaxis_title='Score (%)')

    # Display the plot
    st.plotly_chart(fig)

    # Display the Actual and Predicted data
    st.write("Actual VS Predicted Monkeypox cases model performance.")
    st.write("Confirmed : 0, Suspected : 1, Discarded : 2")
    st.image("image/predicted1.png")
    st.image("image/predicted2.png")

    # Display the evaluation metrics in an interactive table
    st.write("Model Evaluation Metrics Table:")
    st.write(df_metrics)

    st.subheader("Confusion Matrix for Each Model:")

    # Brief explanation on how to interpret the confusion matrix
    st.subheader("Interpreting the Confusion Matrix:")
    st.write("A confusion matrix is a performance measurement tool for machine learning classification algorithms.")
    st.write("It is a table with four different combinations of predicted and actual values: true positives (TP), false positives (FP), true negatives (TN), and false negatives (FN).")
    st.write("From the confusion matrix,various metrics can be calculated, such as accuracy, precision, recall, and F1-score, which provide insights into the model's performance.")
    st.write("For instance, accuracy measures the overall correctness of the model, precision measures the ratio of correctly predicted positive observations to the total predicted positives, recall measures the ratio of correctly predicted positive observations to the all observations in actual class, and F1-score is the harmonic mean of precision and recall.")
    st.write("A higher value of these metrics indicates better model performance.")

    st.image("image/RFcm.png")
    st.image("image/xgbcm.png")
    st.image("image/dtcm.png")

    # Display recommended best-performing model with visualization and justification
    st.subheader("Recommended Best-Performing Model:")
    st.write("Based on the evaluation metrics, the Random Forest model is recommended as the best-performing model.")
    st.write("Here is a visualization of its performance metrics:")

    # Visualization for the recommended model (Random Forest)
    st.write("Random Forest Performance Metrics:")
    st.write("Accuracy: 96.04%")
    st.write("Precision: 96.31%")
    st.write("Recall: 96.04%")
    st.write("F1-score: 96.13%")
    st.write("AUC-ROC: 99.27%")




# About wep app section
def display_about():
    st.title("About")
    st.write("This web application is created for visualizing the impact and spread of Monkeypox using data-driven insights.")
    st.title("Ethical Issues and Considerations")
    st.write("""As a sole researcher leading this study on monkeypox, it is imperative to address the ethical considerations associated with the utilization of the Kaggle dataset. This acknowledgment aims to inform both the public and stakeholders about the ethical framework guiding this research endeavours.
1.	Responsible Data Usage: This research strictly adheres to the terms of use and licensing agreements stipulated by Kaggle for the dataset utilized. It recognizes and respects the intellectual property rights of data contributors, committing to utilizing the data responsibly and ethically.
2.	Data Privacy and Confidentiality: Prioritizing the protection of individuals’ privacy and confidentiality represented in the dataset, the research takes measures to anonymize or de-identify personal information. This ensures the safeguarding of data privacy rights and prevents any unintended disclosures.
3.	Informed Consent: While the Kaggle dataset may comprise publicly available data, this research recognizes and respects the original consent obtained by data contributors for the use of their data in research.
4.	Data Integrity and Accuracy: Ensuring the integrity and accuracy of the dataset is paramount in this research. Thorough data validation processes was conducted to verify the reliability of the sources, identify any biases or errors, and transparently report any limitations or uncertainties.
5.	Responsible Data Sharing: Research commitment extends to responsible data sharing practices. Should the researcher choose to share or publish the findings based on the Kaggle dataset, it is done in accordance with open data principles, ensuring proper documentation and compliance with legal and ethical guidelines.
6. Assurance of User Data Protection: This research guarantees the protection of sensitive user information, such as usernames and passwords. These data elements will be stringently protected, will not be shared with any third party, and will be exclusively used for the purposes of this research. Comprehensive security measures are in place to prevent unauthorized access and ensure the confidentiality and integrity of user data.
""")


# Logout section
def show_logout_button():
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.sidebar.success("You have been logged out.")
        st.experimental_rerun()
        

# Login section
def login_user_interface():
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.button("Login"):
        hashed_pswd = generate_hashes(password)
        result = login_user(username, hashed_pswd)
        if result:
            st.session_state['username'] = username
            st.session_state['logged_in'] = True
            st.success(f"Welcome, {username}")
            st.experimental_rerun()
        else:
            st.error("Incorrect Username or Password")

# New user signup section
def signup_user_interface():
    new_username = st.sidebar.text_input("Choose a username", key='new_username')
    new_password = st.sidebar.text_input("Create a password", type='password', key='new_password')
    confirm_password = st.sidebar.text_input("Confirm password", type='password', key='confirm_password')
    if new_password and new_password == confirm_password:
        if st.sidebar.button("Create Account"):
            hashed_new_password = generate_hashes(new_password)
            add_userdata(new_username, hashed_new_password)
            st.success("You have successfully created a new account! Please login.")
    elif new_password != confirm_password:
        st.error("Passwords do not match!")

def main():
    #display_home_page()
    st.info("Follow the Top left arrow to access the menu bar..")
    if 'logged_in' not in st.session_state:
        st.sidebar.title("Login/Signup")
        option = st.sidebar.selectbox("Login/Signup", ["Login", "Signup"])
        if option == "Signup":
            signup_user_interface()
        else:
            login_user_interface()
    else:
        menu_selection = create_sidebar_menu()
        show_logout_button()  # Display the logout button in the sidebar
        if menu_selection == "Home":
            display_home_page()
        elif menu_selection == "Data Visualization":
            display_data_visualization()
        elif menu_selection == "Model Evaluation":
            display_model_evaluation()
        elif menu_selection == "About":
            display_about()

if __name__ == "__main__":
    main()