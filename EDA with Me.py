import streamlit as st
# import the required libraries
from langchain.llms.openai import OpenAI  # Import OpenAI class for interacting with OpenAI API
import pandas as pd
import plotly.graph_objects as go

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

st.title("Exploratory Data Analysis with Me")  # Set the title of the Streamlit page

# Setup agent with OpenAI API key, setting temperature to 0 for deterministic responses, and disable streaming
if "llm" not in st.session_state or st.session_state["llm"] is None:
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0, streaming=False)
    st.session_state["llm"] = llm
else:
    llm = st.session_state["llm"]



# Read database with pandas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
if "pandas_df" not in st.session_state or st.session_state.get("pandas_df") is None:
    df = pd.read_sql("SELECT * FROM titanic", db._engine)
    st.session_state["pandas_df"] = df
else:
    df = st.session_state["pandas_df"]

# Basic Statistics
st.write("Basic Statistics")
st.write(df.describe())

# Set Seaborn style
sns.set(style="whitegrid")

# Visualizations
# st.subheader("Visualizations")

# st.sidebar.title("Select Visual Charts")
# chart_visual = st.sidebar.selectbox('Select Charts/Plot type',  
#                                     ('Line Chart', 'Bar Chart', 'Bubble Chart')) 
  
# st.sidebar.checkbox("Show Analysis by Survival Status", True, key = 1) 
# selected_status = st.sidebar.selectbox('Select Survival Status', 
#                                        options = ['Survived', 'Not Survived']) 

# fig = go.Figure()
# if chart_visual == 'Line Chart':
#     if selected_status == 'Survived':
#         df_survived = df[df['Survived'] == 1]
#         fig.add_trace(go.Bar(x=df_survived['Age'], y=df_survived['Fare'], name='Age vs Survived'))
#     else:
#         df_survived = df[df['Survived'] == 0]
#         fig.add_trace(go.Scatter(x=df_survived['Age'], y=df_survived['Fare'], name='Age vs Not Survived'))

# st.plotly_chart(fig, use_container_width=True)


# Create columns for side-by-side layout
col1, col2, col3 = st.columns(3)

# Function to create and display plots with adjusted sizes and padding
def display_plot(fig, ax, title, col):
    ax.set_title(title)
    fig.tight_layout(pad=2.0)  # Adjust the padding
    col.pyplot(fig)

# Survival Count
fig, ax = plt.subplots(figsize=(6, 3))  # Adjust the figure size
sns.countplot(x='Survived', data=df, ax=ax)
display_plot(fig, ax, "Survival Count", col1)

# Passenger Class Distribution
fig, ax = plt.subplots(figsize=(6, 3))  # Adjust the figure size
sns.countplot(x='Pclass', data=df, ax=ax)
display_plot(fig, ax, "Passenger Class Distribution", col2)

# Age Distribution
fig, ax = plt.subplots(figsize=(6, 3))  # Adjust the figure size
sns.histplot(df['Age'].dropna(), kde=True, ax=ax)
display_plot(fig, ax, "Age Distribution", col3)

# Additional Visualizations
st.write("### Additional Visualizations")

# Gender Distribution of Survivors
col4, col5 = st.columns(2)

fig, ax = plt.subplots(figsize=(6, 3))  # Adjust the figure size
sns.countplot(x='Survived', hue='Sex', data=df, ax=ax)
display_plot(fig, ax, "Gender Distribution of Survivors", col4)

# Fare Distribution by Class
fig, ax = plt.subplots(figsize=(6, 3))  # Adjust the figure size
sns.boxplot(x='Pclass', y='Fare', data=df, ax=ax)
display_plot(fig, ax, "Fare Distribution by Class", col5)

