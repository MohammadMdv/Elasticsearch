import streamlit as st
from ..utils.api_client import APIClient


def search_interface(api_client: APIClient):
    st.title("Search Interface")

    st.subheader("Normal Search")
    index_name = st.text_input("Index Name for Search")

    if index_name:
        response = api_client.get_index_mapping(index_name)
        if 'error' in response:
            st.error(f"Error: {response['error']}")
        else:
            fields = response[index_name]['mappings']['properties']
            field_names = list(fields.keys())

            st.write("Searchable Fields:")
            query = {}

            for field_name in field_names:
                field_type = fields[field_name]['type']
                if field_type in ["text", "keyword"]:
                    query[field_name] = st.text_input(f"Search {field_name} ({field_type})")

            if st.button("Search"):
                query_dict = {
                    "bool": {
                        "must": [{"match": {field: value}} for field, value in query.items() if value]
                    }
                }
                try:
                    response = api_client.search(index_name, query_dict)
                    st.write(response)
                except Exception as e:
                    st.error(f"Error: {e}")

    st.subheader("Semantic Search")
    semantic_index_name = st.text_input("Index Name for Semantic Search")

    if semantic_index_name:
        vector_fields_response = api_client.get_vector_fields(semantic_index_name)
        if 'error' in vector_fields_response:
            st.error(f"Error: {vector_fields_response['error']}")
        else:
            vector_fields = vector_fields_response["vector_fields"]
            if vector_fields:
                st.write("Vector Fields:")
                field = st.selectbox("Vector Field", vector_fields)
                query_vector_list = api_client.generate_embedding(st.text_input("Query Text"))

                k = st.number_input("Number of Results (k)", min_value=1, step=1)
                num_candidates = st.number_input("Number of Candidates", min_value=1, value=500)
                semantic_query = {
                    "index_name": semantic_index_name,
                    "query": {
                        "field": field,
                        "query_vector": query_vector_list,
                        "k": k,
                        "num_candidates": num_candidates
                    }
                }

                if st.button("Search (Semantic)"):
                    try:
                        response = api_client.knn_search(semantic_query)
                        st.write(response)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("No vector fields available for semantic search.")
