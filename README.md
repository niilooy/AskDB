# AskDB: Your Natural Language Interface for SQL Queries

## Introduction
AskDB is a Streamlit web application, built with Python and powered by Langchain and OpenAI. It's designed to analyze SQL databases, Excel Sheets, and CSV files, and deliver valuable data insights without the need for manual query writing. Users can request information in simple language, and the application will automatically fetch the necessary data along with the corresponding SQL query.

## How It Works

1. The user asks a question.
2. The application generates a descriptive message about the database by feeding the first three rows from all tables within the database to a Language Model (specifically, gpt-3.5-turbo).
3. The SQL query is crafted and executed.
   - The SQL Agent formulates an SQL query based on the user's input.
   - This query is retrieved via a callback handler and run against the database to gather the required information.
4. The application uses the fetched data and the original user question to formulate a comprehensive response.
5. Users are given the option to modify the auto-generated SQL query and execute it again, allowing for customization and refinement of the results.
6. The fetched data can be visualized as bar, line, or scatter plots, or downloaded as a CSV file for further analysis.

## Note on Usage
Due to the cost of OpenAI API keys, the app may not always run with full functionality. However, if you do wish to try it out, feel free to check it out and run in your local. Just place your api key in the secrets.toml file inside .streamlit directory and it should work fine! (Assuming that all the dependencies have already been installed and a virtual environment is created). Thanks for understanding!

Feel free to try the app here:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://askdb-niilooy.streamlit.app)