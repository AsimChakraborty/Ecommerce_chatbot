# import streamlit as st
# from src.utils.data_preprocessing import load_and_preprocess_data
# from src.multi_agent_system import initialize_multi_agent_system

# # Setting page configuration
# st.set_page_config(page_title="E-commerce Customer Behavior Chatbot", layout="wide")

# # Initializing session state
# if 'df' not in st.session_state:
#     st.session_state.df = None
#     st.session_state.process_query = None

# # Loading data
# @st.cache_data
# def load_data():
#     return load_and_preprocess_data("data/E-commerce Customer Behavior - Sheet1.csv")

# # Initializing multi-agent system
# def init_agents():
#     df = load_data()
#     process_query, updated_df = initialize_multi_agent_system(df)
#     st.session_state.df = updated_df
#     st.session_state.process_query = process_query

# # Main app
# # st.title("E-commerce Customer Behavior Chatbot")

# # Sidebar for customer ID
# customer_id = st.sidebar.number_input("Enter Customer ID", min_value=101, max_value=450, step=1, value=101)

# # Initializing agents if not already done
# if st.session_state.process_query is None:
#     init_agents()

# # Chat interface
# st.subheader("Chat with the Bot")
# query = st.text_input("Enter your query (e.g., 'Analyze customer behavior' or 'Recommend for customer')")

# if st.button("Submit Query"):
#     if query:
#         response = st.session_state.process_query(query, customer_id)
#         st.write("**Bot Response:**")
#         st.write(response)
#     else:
#         st.write("Please enter a query.")

# # Displaying customer data
# if st.session_state.df is not None:
#     st.subheader(f"Customer Data (ID: {customer_id})")
#     customer_data = st.session_state.df[st.session_state.df['Customer ID'] == customer_id]
#     if not customer_data.empty:
#         st.dataframe(customer_data)
#     else:
#         st.write("Customer ID not found.")






# import streamlit as st
# from src.utils.data_preprocessing import load_and_preprocess_data
# from src.multi_agent_system import initialize_multi_agent_system

# # Set page configuration
# st.set_page_config(page_title="E-commerce Customer Behavior Chatbot", layout="wide")

# # Initialize session state
# if 'df' not in st.session_state:
#     st.session_state.df = None
#     st.session_state.process_query = None
#     st.session_state.error = None

# # Load data and initialize agents
# @st.cache_resource
# def init_agents():
#     try:
#         df = load_and_preprocess_data("data/E-commerce Customer Behavior - Sheet1.csv")
#         process_query, updated_df = initialize_multi_agent_system(df)
#         return process_query, updated_df
#     except Exception as e:
#         st.session_state.error = f"Error initializing agents: {str(e)}"
#         return None, None

# # Main app
# # st.title("E-commerce Customer Behavior Chatbot")

# # Initialize agents if not already done
# if st.session_state.process_query is None:
#     st.session_state.process_query, st.session_state.df = init_agents()

# # Display initialization error if any
# if st.session_state.error:
#     st.error(st.session_state.error)
#     st.stop()

# # Sidebar for customer ID and query examples
# st.sidebar.header("Input Options")
# customer_id = st.sidebar.number_input("Enter Customer ID (optional, for recommendations)", min_value=101, max_value=450, step=1, value=101)
# # Chat interface
# st.subheader("Chat with the Bot")
# query = st.text_input("Enter your query (e.g., 'Analyze customer behavior' or 'Recommend for customer')")

# if st.button("Submit Query"):
#     if query:
#         with st.spinner("Processing query..."):
#             response = st.session_state.process_query(query, customer_id if "recommend" in query.lower() else None)
#         st.write("**Bot Response:**")
#         st.write(response)
#     else:
#         st.warning("Please enter a query.")

# # Display customer data
# if st.session_state.df is not None:
#     st.subheader(f"Customer Data (ID: {customer_id})")
#     customer_data = st.session_state.df[st.session_state.df['Customer ID'] == customer_id]
#     if not customer_data.empty:
#         st.dataframe(customer_data, use_container_width=True)
#     else:
#         st.warning("Customer ID not found.")

# # Display dataset overview
# # st.subheader("Dataset Overview")
# # if st.session_state.df is not None:
# #     st.write(f"Total Customers: {len(st.session_state.df)}")
# #     st.dataframe(st.session_state.df.head(), use_container_width=True)





import streamlit as st
from src.utils.data_preprocessing import load_and_preprocess_data
from src.multi_agent_system import initialize_multi_agent_system
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="E-commerce Customer Behavior Chatbot", layout="wide")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
    st.session_state.process_query = None
    st.session_state.error = None

# Load data and initialize agents
@st.cache_resource
def init_agents():
    try:
        df = load_and_preprocess_data("data/E-commerce Customer Behavior - Sheet1.csv")
        process_query, updated_df = initialize_multi_agent_system(df)
        return process_query, updated_df
    except Exception as e:
        st.session_state.error = f"Error initializing agents: {str(e)}"
        return None, None

# Function to log prompt to prompt.txt
def log_prompt(query):
    try:
        with open("prompt.txt", "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {query}\n")
    except Exception as e:
        st.warning(f"Error logging prompt: {str(e)}")

# Main app
# st.title("E-commerce Customer Behavior Chatbot")

# Initialize agents if not already done
if st.session_state.process_query is None:
    st.session_state.process_query, st.session_state.df = init_agents()

# Display initialization error if any
if st.session_state.error:
    st.error(st.session_state.error)
    st.stop()

# Sidebar for customer ID and query examples
st.sidebar.header("Input Options")
customer_id = st.sidebar.number_input("Enter Customer ID (optional, for recommendations)", min_value=101, max_value=450, step=1, value=101)

# Chat interface
st.subheader("Chat with the Bot")
query = st.text_input("Enter your query (e.g., 'Analyze customer behavior' or 'Recommend for customer')")

if st.button("Submit Query"):
    if query:
        # Log the prompt to prompt.txt
        log_prompt(query)
        with st.spinner("Processing query..."):
            response = st.session_state.process_query(query, customer_id if "recommend" in query.lower() else None)
        st.write("**Bot Response:**")
        st.write(response)
    else:
        st.warning("Please enter a query.")

# Display customer data
if st.session_state.df is not None:
    st.subheader(f"Customer Data (ID: {customer_id})")
    customer_data = st.session_state.df[st.session_state.df['Customer ID'] == customer_id]
    if not customer_data.empty:
        st.dataframe(customer_data, use_container_width=True)
    else:
        st.warning("Customer ID not found.")







