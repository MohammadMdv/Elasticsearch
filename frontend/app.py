import streamlit as st
from utils.api_client import APIClient
from components.index_management import index_management
from components.document_management import document_management
from components.search_interface import search_interface

api_client = APIClient("http://localhost:8000")

st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ["Index Management", "Document Management", "Search"])

if options == "Index Management":
    index_management(api_client)
elif options == "Document Management":
    document_management(api_client)
elif options == "Search":
    search_interface(api_client)
