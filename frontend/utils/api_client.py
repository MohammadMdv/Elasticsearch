import requests
import json

from requests import RequestException


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_index(self, index_name, mapping):
        data = {"index_name": index_name, "mapping": mapping}
        print(f"Sending request to {self.base_url}/create_index/")
        print(f"Request data: {json.dumps(data, indent=2)}")
        try:
            response = requests.post(f"{self.base_url}/create_index/", json=data, timeout=30)
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return response.json()
        except RequestException as e:
            print(f"Request failed: {e}")
            return {"error": str(e)}

    def delete_index(self, index_name):
        response = requests.delete(f"{self.base_url}/delete_index/", params={"index_name": index_name})
        return response.json()

    def insert_document(self, index_name, body, doc_id=None):
        data = {"index_name": index_name, "body": body}
        if doc_id:
            data["doc_id"] = doc_id
        response = requests.post(f"{self.base_url}/insert_document/", json=data)
        return response.json()

    def delete_document(self, index_name, doc_id):
        response = requests.delete(f"{self.base_url}/delete_document/",
                                   params={"index_name": index_name, "doc_id": doc_id})
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

    def create_embeddings(self, text):
        response = requests.post(f"{self.base_url}/create_embeddings/", json={"text": text})
        return response.json()

    def get_index_mapping(self, index_name):
        response = requests.get(f"{self.base_url}/get_index_mapping/{index_name}")
        return response.json()

    def get_vector_fields(self, index_name):
        response = requests.get(f"{self.base_url}/get_vector_fields/{index_name}")
        return response.json()
