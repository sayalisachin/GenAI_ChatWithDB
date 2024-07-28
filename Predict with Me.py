import streamlit as st 
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler  # Callback handler for integrating with Streamlit UI
import pandas as pd
from langchain.llms.openai import OpenAI  # Import OpenAI class for interacting with OpenAI API
from langchain.agents.agent_types import AgentType  # Enum for specifying the type of agent to create
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn

# Check if openai_api_key is not entered and display a warning message
if  "openai_api_key" not in st.session_state or st.session_state.get("openai_api_key") is None:
    st.warning("Please input your OpenAI API Key")  # Show warning in the Streamlit app
    st.stop()  # Stop execution if no API key is entered
else:
    openai_api_key = st.session_state["openai_api_key"]  # Retrieve the API key from session state
    st.sidebar.write("You are now ready to use the OpenAI API")  # Confirmation message for API key input

# Check if the database is connected and display an error message if not
if "database" not in st.session_state or st.session_state.get("database") is None:
    st.error("Please connect to the database first.")  # Show error in the Streamlit app
    st.stop()  # Stop execution if the database is not connected
else:
    db = st.session_state["database"]  # Retrieve the database connection from session state
    st.sidebar.write("You are now connected to the database")  # Confirmation message for database connection

st.title("Predict with Me")  # Set the title of the Streamlit page

if "pandas_df" not in st.session_state or  st.session_state.get("pandas_df") is None:
    df = pd.read_sql("SELECT * FROM titanic", db._engine)
    st.session_state["pandas_df"] = df
else:
    df = st.session_state["pandas_df"]


if "llm" not in st.session_state or st.session_state["llm"] is None:
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0, streaming=False)
    st.session_state["llm"] = llm
else:
    llm = st.session_state["llm"]

# Create an agent with the Pandas DataFrame toolkit, specifying agent type and verbosity
agent = create_pandas_dataframe_agent(
    llm=llm, 
    df=df,
    verbose=True,  # Enable verbose output for debugging
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Specify the agent type for handling queries
    allow_dangerous_code=True,  # Allow dangerous code execution
)

# Initialize or clear message history based on user action
if "messages" not in st.session_state or st.sidebar.button("Clear message history  🧹"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]  # Default message

user_query = st.chat_input(placeholder="Ask me anything...")  # Input field for user queries

# Handle user query
if user_query:
    st.session_state["messages"].append({"role": "user", "content": user_query})  # Add user query to message history
    st.chat_message("user").write(user_query)  # Display user query in chat UI

    with st.chat_message("assistant"):  # Assistant's response block
        st_cb = StreamlitCallbackHandler(st.container())  # Initialize Streamlit callback handler
        response = agent.run(user_query, callbacks=[st_cb])  # Run the agent to get a response
        st.session_state["messages"].append({"role": "assistant", "content": response})  # Add response to history
        st.write(response)  # Display the assistant's response