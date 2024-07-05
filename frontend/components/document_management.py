import streamlit as st
from utils.api_client import APIClient


def document_management(api_client: APIClient):
    st.subheader("Insert Document")
    index_name = st.text_input("Index Name")

    if index_name:
        mapping = api_client.get_index_mapping(index_name)

        document = {}
        semantic_fields = []
        fields = mapping[index_name]['mappings']['properties']
        for field_name in list(fields.keys()):
            if not field_name.endswith("_vector"):
                field_type = fields[field_name]["type"]
                if field_type == "text" or field_type == "keyword":
                    document[field_name] = st.text_input(f"{field_name} (text)")
                    if f"{field_name}_vector" in list(fields):
                        semantic_fields.append(field_name)
                elif field_type == "integer":
                    document[field_name] = st.number_input(f"{field_name} (integer)", step=1)
                elif field_type == "float":
                    document[field_name] = st.number_input(f"{field_name} (float)", step=0.1)
                elif field_type == "date":
                    document[field_name] = st.date_input(f"{field_name} (date)")

        if st.button("Insert Document"):
            response = api_client.insert_document(index_name, document, semantic_fields)
            st.write(response)
