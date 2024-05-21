## Author: Musiliu Bello
## Student-ID B1210259
## School of Computing, Engineering and Digital Technologies , Teesside University, Middlesbrough United Kingdom.



This readme provides instructions to run the second approach, which utilizes a Python-based framework for disease mitigation using machine learning (ML) and web app visualization.

Prerequisites

Software:
Python 3.x (Download from: https://www.python.org/downloads/)
Jupyter Notebook (Installation instructions: https://jupyter.org/)
Visual Studio Code (Download from: https://code.visualstudio.com/)
Streamlit (Installation: pip install streamlit)
SQLite (Database available with most Python installations)
Hardware: A computer with sufficient processing power and memory is recommended.

Project Structure

The project consists of several components:

Jupyter Notebook(s): These notebooks contain Python code for data processing, model training, and evaluation.
Streamlit App: This web application allows users to interact with the dataset, various monkeypox case analysis, and implemented models results visualization and performance metrics.
SQLite3 Database: This database stores user registration and login data for the Streamlit app(Web data security).

Running the Code

Jupyter Notebook:
Open Jupyter Notebook and navigate to the directory containing the notebook source codes.
Double-click the notebook files one after the other to launch it in the Jupyter Notebook interface(Stage1_MonkeypoxML_Case_Analysis, Stage2_MonkeypoxML_DataCleaning, Stage3_MonkeypoxML_Preprocessing_Modelling, Stage4_MonkeypoxML_FeaturesScaling_Hyperparameter_Modelling).
Execute the code cells (blocks of code) sequentially by pressing Shift + Enter or clicking the "Run" button in the toolbar.
This will likely involve data loading,monkeypox dataset cases visualization, pre-processing, model training, and evaluation steps through stage1 - stage4.
Streamlit App:
Navigate to the same source code directory containing the Streamlit app script (webpage.py).
Open a terminal or command prompt and navigate to the same directory.
Run the script using the command: streamlit run path/webpage.py (Replace "path" with the actual file path).
This will launch the Streamlit app in your web browser, typically at http://localhost:8501/.

The webpage will allow users to:

Register as a new user through the sidebar menu.
Login if they are existing users, also using the sidebar menu.
Visualize the Monkeypox dataset: This could involve charts, graphs, or tables that explore various aspects of the data.
Explore analyses of Monkeypox cases: This might include breakdowns by demographics, location, or other relevant factors.
View the results of implemented models: This involves visualizations of model predictions or comparisons between different models.
Analyze model performance metrics: This includes accuracy, precision, recall, F1-Score and AUC_RUC or other metrics used to evaluate the models like Confusion Matrix.

For any difficulties or suggestions, please contact the author.

Thank you.