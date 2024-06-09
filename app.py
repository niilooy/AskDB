import streamlit as st
from langchain_community.utilities import SQLDatabase
import tempfile
from sql_agent import SQLAgent
import pandas as pd
import sqlite3

def run_query(query):
    '''Run custom or LLM generated query and return the result as a dataframe'''
    try:
        result_cursor = db.run(query, fetch="cursor")
        data = result_cursor.fetchall()
        columns = result_cursor.keys()
        df = pd.DataFrame(data, columns=columns)
        return df
    except:
        return None

def load_file_to_sqlite(file, file_type):
    '''Load CSV, XLSX, or XLS file to SQLite database'''
    if file_type == "csv":
        df = pd.read_csv(file)
    elif file_type == "xlsx":
        df = pd.read_excel(file, engine='openpyxl')
    elif file_type == "xls":
        df = pd.read_excel(file, engine='xlrd')
    else:
        raise ValueError("Unsupported file type")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp_file:
        conn = sqlite3.connect(tmp_file.name)
        df.to_sql('data', conn, index=False, if_exists='replace')
        conn.close()
        return tmp_file.name

def get_table_schema(table_name):
    '''Get the schema and foreign keys of a table'''
    # Get the schema
    schema_query = f"PRAGMA table_info({table_name})"
    schema_cursor = db.run(schema_query, fetch="cursor")
    schema_data = schema_cursor.fetchall()
    schema_columns = schema_cursor.keys()
    schema_df = pd.DataFrame(schema_data, columns=schema_columns)

    # Get the foreign keys
    fk_query = f"PRAGMA foreign_key_list({table_name})"
    fk_cursor = db.run(fk_query, fetch="cursor")
    fk_data = fk_cursor.fetchall()
    fk_columns = fk_cursor.keys()
    fk_df = pd.DataFrame(fk_data, columns=fk_columns) if fk_data else None

    return schema_df, fk_df

def show_schema_details_expander():
    schema_expander = st.expander("Show Schemas")
    schema_details = ""  # Initialize an empty string to store schema details
    with schema_expander:
        for table_name in table_names:
            st.write(f"Table: {table_name}")
            schema_df, fk_df = get_table_schema(table_name)
            schema_details += f"Table: {table_name}\nSchema:\n" + schema_df.to_string() + "\n"
            st.write("Schema:")
            st.write(schema_df)
            if fk_df is not None:
                schema_details += "Foreign Keys:\n" + fk_df.to_string() + "\n\n"
                st.write("Foreign Keys:")
                st.write(fk_df)
            else:
                schema_details += "Foreign Keys: None\n\n"
        st.session_state['schema_details'] = schema_details  # Store the schema details in the session state

def vizualize_data(query):
    '''Visualize the result of the query'''

    # Retrieve DataFrame from the query
    df = run_query(query)
    if df is None:
        # If the query is invalid, show an error message
        st.error('Query Error, please try again...')
        return
    
    # Column 2 used only for the download button
    visualization, download = st.columns([0.7, 0.3])

    # Visualization column (Column 1)
    popover = visualization.popover('Visualization')
    # Select the type of visualization
    choice = popover.selectbox("Select visualization", ["Table", "Bar chart", "Line chart", "Scatter chart"])

    if choice == "Table":
        st.write(df)
        # Column 2 used only for the download button
        download.download_button("Download as csv", df.to_csv(), "data.csv", "text/csv")

    else:
        # Select the x and y axis to display in the charts
        x = popover.selectbox("Select x-axis", df.columns, index=0)
        y = popover.selectbox("Select y-axis", df.columns, index=1)

        # Display the selected chart
        if choice == "Bar chart":
            st.bar_chart(df, x=x, y=y)
        elif choice == "Line chart":
            st.line_chart(df, x=x, y=y)
        elif choice == "Scatter chart":
            st.scatter_chart(df, x=x, y=y)

# Before File Upload - Start of the app, ask the user to upload a database if not present
if "tmp_file_path" not in st.session_state:
    # Set layout for better UI
    st.set_page_config(layout="centered", page_title='AskDB! ✨')
    st.title("AskDB! ✨")
    data = st.file_uploader("Upload Database, CSV, or Excel File", type=["db", "csv", "xlsx", "xls"])
    if data:
        if data.name.endswith('.csv'):
            st.session_state['tmp_file_path'] = load_file_to_sqlite(data, "csv")
        elif data.name.endswith('.xlsx'):
            st.session_state['tmp_file_path'] = load_file_to_sqlite(data, "xlsx")
        elif data.name.endswith('.xls'):
            st.session_state['tmp_file_path'] = load_file_to_sqlite(data, "xls")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp_file:
                tmp_file.write(data.getvalue())
                st.session_state['tmp_file_path'] = tmp_file.name
        st.rerun()
    button_demo = st.button("Use demo database")
    if button_demo:
        st.session_state['tmp_file_path'] = "data/chinook.db"
        st.rerun()

# After File Upload - If the database is uploaded, show the SQL query tool
if "tmp_file_path" in st.session_state:
    st.set_page_config(layout="wide", page_title='AskDB! ✨')

    # Initialize and use the database
    db = SQLDatabase.from_uri(f"sqlite:///{st.session_state['tmp_file_path']}")

    # Used for the header only
    title, button = st.columns([0.85, 0.15])
    title.title("Data Insights")
    button.button("Reset database", on_click=lambda: st.session_state.pop("tmp_file_path"), type="primary")

    # Main layout
    cont1 = st.container()

    # Split the layout into two columns, one for the visualization and the other for the SQL query
    col1, col2 = cont1.columns([0.6, 0.4])
    
    # We start by defining the column 2 that contains the SQL query tool as it is important for the execution order
    with col2:
        st.header("Run Query")

        # Create a text area for the query and fill it with the custom or LLm generated query
        if 'query' not in st.session_state:
            query = st.text_area("Enter your SQL query here")
        else:
            query = st.text_area("Enter your SQL query here", st.session_state['query'])
        
        # Create a button to run the custom query
        run_query_button = st.button("Run query")

        if 'query_output' in st.session_state:
            # Create container to display the output of the LLM with fixed height
            container_output = st.container(height=190)
            container_output.write(st.session_state['query_output'])
    
    # Column 1 contains the visualization of the query
    with col1:
        # If query is not run, show the tables in the database, show the schemas and keep them ready for the prompt
        if 'query' not in st.session_state and not run_query_button:
            st.write("Tables in the database:")
            table_names = db.get_usable_table_names()
            st.write(table_names)
            show_schema_details_expander()
                
        else:
            if not run_query_button:
                # Run LLM generated query and show visualization
                vizualize_data(st.session_state['query'])
                st.write("Run an Empty Query to go back to Schema View")
            else:
                if query:
                    # Run custom query and show visualization
                    st.session_state['query']=query
                    vizualize_data(st.session_state['query'])
                    st.write("Run an Empty Query to go back to Schema View")
                else:
                    # If query is empty, show the tables and schemas in the database
                    table_names = db.get_usable_table_names()
                    st.write(table_names)
                    show_schema_details_expander()

    # Create input to ask LLM to create a query
    prompt = st.chat_input("Enter your question here")

    if prompt:
        # Create loading spinner
        with st.spinner('Wait for it...'):
            try:
                # Create custom SQL agent and ask LLM the question
                agent = SQLAgent(db)
                result = agent.invoke(prompt)

                # Save the output and the query in the session state
                st.session_state['query_output'] = result['output']
                sql_query=agent.get_sql()
                if sql_query:
                    st.session_state['query'] = sql_query[-1]['query']
            except Exception as e:
                # If an error occurs, delete the prompt
                print(e)
                prompt = None
        
        # Rerun the app to show the output and the query
        st.rerun()