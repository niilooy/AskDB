# AskDB: Your Natural Language Interface for SQL Queries 🛠️

## Introduction
**AskDB** is a Streamlit web application built with Python, powered by Langchain and OpenAI. It's designed to analyze SQL databases, Excel Sheets, and CSV files, delivering valuable data insights without the need for manual query writing. Simply ask a question in natural language, and the application will automatically fetch the necessary data along with the corresponding SQL query.

## 🚀 How It Works

1. 🗣️ **Ask a Question**: Users start by posing a question in simple language.
2. 🧠 **Database Description**: The application generates a descriptive overview of the database by feeding the first three rows from all tables to a Language Model (specifically, GPT-3.5-turbo / GPT-4o-mini).
3. 📝 **SQL Query Crafting**: 
   - The SQL Agent formulates an SQL query based on the user's input.
   - This query is retrieved via a callback handler and run against the database to gather the necessary data.
4. 🤖 **Response Generation**: The application uses the fetched data and the original user question to create a comprehensive response.
5. 🎛️ **Customization**: Users have the option to modify the auto-generated SQL query and execute it again, allowing for customization and refinement of results.
6. 📊 **Data Visualization**: The fetched data can be visualized as bar, line, or scatter plots, or downloaded as a CSV file for further analysis.

## 🎥 Demo

### 📤 Upload DB and Show Schemas
[Watch the Demo](https://github.com/user-attachments/assets/e25375d7-911f-4789-9e5f-55109748d5aa)

### 💬 Chats
[See How It Works](https://github.com/user-attachments/assets/d7890dac-9e13-402a-a74d-a4b4c07eb390)

### 💻 Manual Querying
[Explore Manual Querying](https://github.com/user-attachments/assets/87d84b39-bbf2-489e-88c6-94e32116be4f)

### 📈 Auto Querying and Data Visualization
[Watch Auto Querying & Data Visualization](https://github.com/user-attachments/assets/2f36c060-8d25-4e1f-8e1c-f92400cfcf05)

## ⚠️ Note on Usage
Due to the cost of OpenAI API keys, the app may not always run with full functionality. However, if you'd like to try it out, feel free to run it locally! Just place your API key in the `secrets.toml` file inside the `.streamlit` directory, and it should work perfectly! (Assuming that all dependencies have been installed and a virtual environment is set up). Thanks for understanding!

Ready to give it a try? Check out the app here:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://askdb-niilooy.streamlit.app) 🎉
