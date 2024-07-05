import streamlit as st
from utils.api_client import APIClient


def index_management(api_client: APIClient):
    st.subheader("Create Index")
    index_name = st.text_input("Index Name")

    field_count = st.number_input("Number of Fields", min_value=1, max_value=20, step=1)
    fields = []
    semantic_fields = []

    for i in range(field_count):
        st.subheader(f"Field {i + 1}")
        field_name = st.text_input(f"Field Name {i + 1}", key=f"field_name_{i}")
        field_type = st.selectbox(f"Field Type {i + 1}", ["text", "keyword", "integer", "float", "date"],
                                  key=f"field_type_{i}")

        if field_type == "text":
            enable_semantic_search = st.checkbox(f"Enable Semantic Search for {field_name}", key=f"semantic_{i}")
            if enable_semantic_search:
                semantic_fields.append(field_name)

        fields.append({"name": field_name, "type": field_type})

    if st.button("Create Index"):
        mapping = {"properties": {field["name"]: {"type": field["type"]} for field in fields}}
        response = api_client.create_index(index_name, mapping, semantic_fields)
        st.write(response)
