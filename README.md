# AskDB: Your Natural Language Interface for SQL Queries

## Introduction
AskDB is a Streamlit web application, built with Python and powered by Langchain and OpenAI. It's designed to analyze SQL databases, Excel Sheets, and CSV files, and deliver valuable data insights without the need for manual query writing. Users can request information in simple language, and the application will automatically fetch the necessary data along with the corresponding SQL query.

## How It Works

1. The user asks a question.
2. The application generates a descriptive message about the database by feeding the first three rows from all tables within the database to a Language Model (specifically, gpt-3.5-turbo / gpt-4o-mini).
3. The SQL query is crafted and executed.
   - The SQL Agent formulates an SQL query based on the user's input.
   - This query is retrieved via a callback handler and run against the database to gather the required information.
4. The application uses the fetched data and the original user question to formulate a comprehensive response.
5. Users are given the option to modify the auto-generated SQL query and execute it again, allowing for customization and refinement of the results.
6. The fetched data can be visualized as bar, line, or scatter plots, or downloaded as a CSV file for further analysis.

# Demo

## Upload DB and Show Schemas
https://github.com/user-attachments/assets/e25375d7-911f-4789-9e5f-55109748d5aa

## Chats
https://github.com/user-attachments/assets/d7890dac-9e13-402a-a74d-a4b4c07eb390

## Manual Querying
https://github.com/user-attachments/assets/87d84b39-bbf2-489e-88c6-94e32116be4f

## Auto Querying and Data Vizualization
https://github.com/user-attachments/assets/2f36c060-8d25-4e1f-8e1c-f92400cfcf05

## Note on Usage
Due to the cost of OpenAI API keys, the app may not always run with full functionality. However, if you do wish to try it out, feel free to check it out and run in your local. Just place your api key in the secrets.toml file inside .streamlit directory and it should work fine! (Assuming that all the dependencies have already been installed and a virtual environment is created). Thanks for understanding!

Feel free to try the app here:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://askdb-niilooy.streamlit.app)
