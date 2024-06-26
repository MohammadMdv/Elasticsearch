import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_index(self, index_name, mappings):
        response = requests.post(f"{self.base_url}/create_index/",
                                 json={"index_name": index_name, "mappings": mappings})
        return response.json()

    def delete_index(self, index_name):
        response = requests.delete(f"{self.base_url}/delete_index/{index_name}")
        return response.json()

    def insert_document(self, index_name, document):
        response = requests.post(f"{self.base_url}/add_document/{index_name}", json=document)
        return response.json()

    def delete_document(self, index_name, doc_id):
        response = requests.delete(f"{self.base_url}/delete_document/{index_name}/{doc_id}")
        return response.json()

    def search(self, index_name, query):
        response = requests.post(f"{self.base_url}/search/", json={"index_name": index_name, "query": query})
        return response.json()

    def knn_search(self, query):
        response = requests.post(f"{self.base_url}/knn_search/", json=query)
        return response.json()

    def get_available_models(self):
        response = requests.get(f"{self.base_url}/get_available_models/")
        return response.json()

    def set_model(self, model_name):
        response = requests.post(f"{self.base_url}/set_model/", json={"model_name": model_name})
        return response.json()

    def generate_embedding(self, text):
        response = requests.post(f"{self.base_url}/generate_embedding/", json={"text": text})
        return response.json()
