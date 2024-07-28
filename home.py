import streamlit as st
import sqlite3
# from langchain.sql_database import SQLDatabase
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from pathlib import Path

# Warning message about SQL injection vulnerability
INJECTION_WARNING = """
                    SQL agent can be vulnerable to prompt injection. Use a DB role with limited permissions.
                    Read more [here](https://python.langchain.com/docs/security).
                    """
LOCALDB= "USE_LOCALDB"  # Constant for using a local database

# Configure the Streamlit page with a title, icon, layout, and initial sidebar state
st.set_page_config(page_title= "Landing Page", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")
st.title("Welcome to the Landing Page")  # Set the title of the page

# Sidebar input for OpenAI API key with password type input
openai_api_key= st.sidebar.text_input("OpenAI API Key", type="password")

# Check if the OpenAI API key is not entered and display a warning
if not openai_api_key:
    st.warning("Please input your OpenAI API Key")
    st.stop()  # Stop execution if no API key is entered
else:
    st.session_state["openai_api_key"]= openai_api_key

st.sidebar.write("You are now ready to use the OpenAI API")  # Confirmation message for API key input

# Sidebar radio buttons for database selection
radio_opt= ["Use sample database", "Connect to your database"]
selected_opt= st.sidebar.radio(label="Choose suitable option", options=radio_opt)

# Display SQL injection warning if "Connect to your database" is selected
if radio_opt.index(selected_opt) == 1:
    st.sidebar.warning(INJECTION_WARNING, icon="⚠️")
    # Input for database URI with a placeholder
    db_uri = st.sidebar.text_input(
        label="Database URI", placeholder="mysql://user:pass@hostname:port/db"
    )
else:
    db_uri = LOCALDB  # Use local database if the first option is selected

# Check if the database URI is not entered and display information message
if not db_uri:
    st.info("Please enter database URI to connect to your database.")
    st.stop()  # Stop execution if no database URI is entered

def configure_db(db_uri):
    if db_uri == LOCALDB:
        # Make the DB connection read-only to reduce risk of injection attacks
        # See: https://python.langchain.com/docs/security
        db_filepath = (Path(__file__).parent / "titanic.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{db_filepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    return SQLDatabase.from_uri(database_uri=db_uri)

db = configure_db(db_uri)
st.session_state["database"]= db


st.sidebar.write("You are now connected to the database")  # Confirmation message for database connection
st.sidebar.write("You can now use the OpenAI API and the database by using the pages for Chat, EDA and Predictive Analysis")  # Information message for API and database connection
