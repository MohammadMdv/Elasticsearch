import streamlit as st
from utils.api_client import APIClient


def document_management(api_client: APIClient):
    st.title("Document Management")

    st.subheader("Insert Document")
    index_name = st.text_input("Index Name for Insertion")

    if index_name:
        response = api_client.get_index_mapping(index_name)
        fields = response[index_name]['mappings']['properties']
        field_names = list(fields.keys())

        st.write("Available Fields:")
        field_values = {}
        for field_name in field_names:
            field_type = fields[field_name]['type']
            field_value = st.text_input(f"{field_name} ({field_type})", key=f"field_value_{field_name}")
            field_values[field_name] = field_value

        if st.button("Insert Document"):
            try:
                response = api_client.insert_document(index_name, field_values)
                st.write(response)
            except Exception as e:
                st.error(f"Error: {e}")

    st.subheader("Delete Document")
    delete_index_name = st.text_input("Index Name for Deletion")
    doc_id = st.text_input("Document ID to Delete")

    if st.button("Delete Document"):
        response = api_client.delete_document(delete_index_name, doc_id)
        st.write(response)
