from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import google.generativeai as genai
import os
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt, question])
    raw_text = response.text.strip()

    # Extract the SQL line only
    for line in raw_text.splitlines():
        if line.strip().lower().startswith(("select", "insert", "update", "delete", "create")):
            return line.strip()

    # Fallback if nothing is found
    return raw_text

def connect_to_mysql(host, user, password, database=None):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database if database else None
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

def get_databases(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        cursor.close()
        return databases
    except Error as e:
        st.error(f"Error fetching databases: {e}")
        return []

def get_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        return tables
    except Error as e:
        st.error(f"Error fetching tables: {e}")
        return []

def get_table_schema(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        schema = cursor.fetchall()
        cursor.close()
        return [(col[0], col[1]) for col in schema]  # (name, type)
    except Error as e:
        st.error(f"Error fetching schema for {table_name}: {e}")
        return []

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            return rows, columns
        else:
            connection.commit()
            cursor.close()
            return None, None
    except Error as e:
        st.error(f"Error executing query: {e}")
        return None, None

prompt = """
You are an expert in converting English statements into SQL queries for a MySQL database!
The user will specify the database and table they want to query. The table schema is dynamic and not fixed.
Generate SQL queries based on the user's natural language input.

Examples:
1. How many records are in the employees table: SELECT COUNT(*) FROM employees;
2. Get all products with price above 100: SELECT * FROM products WHERE price > 100;
3. Create a table for customers: CREATE TABLE customers (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100));
4. Insert a customer record: INSERT INTO customers VALUES (1, 'John Doe', 'john@example.com');

The SQL query should not have any ... in the beginning or end and should not include the word 'sql' in the output.
Ensure the query matches the table and column names exactly as provided by the user.
"""

# Streamlit App
st.set_page_config(page_title="AstraDB AI")
st.header("Chat with MySQL Database")

# MySQL Connection Inputs
with st.sidebar:
    st.subheader("Connect to MySQL Server")
    host = st.text_input("Host", value="localhost")
    user = st.text_input("Username", value="root")
    password = st.text_input("Password", type="password")
    connect_button = st.button("Connect")

    if 'connection' not in st.session_state:
        st.session_state.connection = None
    if 'database' not in st.session_state:
        st.session_state.database = None

    if connect_button:
        st.session_state.connection = connect_to_mysql(host, user, password)
        if st.session_state.connection:
            st.success("Connected to MySQL server!")
            st.session_state.database = None  # Reset database selection

# Database Selection
    if st.session_state.connection:
        databases = get_databases(st.session_state.connection)
        selected_db = st.selectbox("Select Database", [""] + databases, key="db_select")
        if selected_db and selected_db != st.session_state.database:
            st.session_state.database = selected_db
            st.session_state.connection = connect_to_mysql(host, user, password, selected_db)
            if st.session_state.connection:
                st.success(f"Connected to database: {selected_db}")

# Tabs for different functionalities
if st.session_state.connection and st.session_state.database:
    tables = get_tables(st.session_state.connection)
    tab1, tab2, tab3 = st.tabs(["Query Database", "Create Table", "Insert Data"])

    with tab1:
        st.subheader("Query Database with Natural Language")
        selected_table = st.selectbox("Select Table", [""] + tables, key="query_table")
        if selected_table:
            schema = get_table_schema(st.session_state.connection, selected_table)
            st.write("Table Schema:")
            st.table(pd.DataFrame(schema, columns=["Column Name", "Data Type"]))
        question = st.text_input("Input your question", key="query_input")
        submit = st.button("Ask")
        if submit and question and selected_table:
            response = get_gemini_response(question, prompt)
            st.write("Generated SQL Query: " + response)
            rows, columns = execute_query(st.session_state.connection, response)
            if rows and columns:
                st.subheader("Results:")
                st.table(pd.DataFrame(rows, columns=columns))

    with tab2:
        st.subheader("Create a New Table")
        table_name = st.text_input("Table Name")
        table_schema = st.text_area(
            "Table Schema (e.g., id INT PRIMARY KEY, name VARCHAR(100))",
            value=""
        )
        create_button = st.button("Create Table")
        if create_button and table_name and table_schema:
            query = f"CREATE TABLE {table_name} ({table_schema})"
            execute_query(st.session_state.connection, query)
            st.success(f"Table {table_name} created successfully!")
            # Refresh table list
            tables = get_tables(st.session_state.connection)

    with tab3:
        st.subheader("Insert Data")
        selected_table = st.selectbox("Select Table", [""] + tables, key="insert_table")
        if selected_table:
            schema = get_table_schema(st.session_state.connection, selected_table)
            st.write("Table Schema:")
            st.table(pd.DataFrame(schema, columns=["Column Name", "Data Type"]))
            # Dynamic input fields based on schema
            input_data = {}
            for col_name, col_type in schema:
                if "int" in col_type.lower():
                    input_data[col_name] = st.number_input(f"{col_name} ({col_type})", step=1)
                elif "float" in col_type.lower() or "double" in col_type.lower():
                    input_data[col_name] = st.number_input(f"{col_name} ({col_type})")
                else:
                    input_data[col_name] = st.text_input(f"{col_name} ({col_type})")
            insert_button = st.button("Insert Record")
            if insert_button:
                columns = ", ".join(input_data.keys())
                values = []
                for val in input_data.values():
                    if isinstance(val, (int, float)):
                        values.append(str(val))
                    else:
                        values.append(f"'{val}'")
                values_str = ", ".join(values)
                query = f"INSERT INTO {selected_table} ({columns}) VALUES ({values_str})"
                execute_query(st.session_state.connection, query)
                st.success("Record inserted successfully!")