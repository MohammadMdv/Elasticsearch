import streamlit as st
from utils.api_client import APIClient


def index_management(api_client: APIClient):
    st.title("Index Management")

    st.subheader("Create Index")
    index_name = st.text_input("Index Name")

    field_count = st.number_input("Number of Fields", min_value=1, max_value=20, step=1)
    fields = []
    for i in range(field_count):
        st.subheader(f"Field {i + 1}")
        field_name = st.text_input(f"Field Name {i + 1}", key=f"field_name_{i}")
        field_type = st.selectbox(f"Field Type {i + 1}", ["text", "keyword", "integer", "float", "date"],
                                  key=f"field_type_{i}")
        fields.append({"name": field_name, "type": field_type})

    if st.button("Create Index"):
        try:
            mapping = {
                "properties": {
                    field["name"]: {"type": field["type"]} for field in fields
                }
            }
            response = api_client.create_index(index_name, mapping)
            st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Delete Index")
    delete_index_name = st.text_input("Index Name to Delete")

    if st.button("Delete Index"):
        response = api_client.delete_index(delete_index_name)
        st.write(response)
