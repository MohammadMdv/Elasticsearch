from fastapi import FastAPI
from .services.elasticsearch_service import ElasticsearchService

app = FastAPI()
es_service = ElasticsearchService()


@app.post("/create_index/")
def create_index(index_name: str, mapping: dict):
    return es_service.create_index(index_name, mapping)


@app.post("/insert_document/")
def insert_document(index_name: str, document: dict, doc_id: str = None):
    return es_service.insert_one_document(index_name, document, doc_id)


@app.get("/get_document/")
def get_document(index_name: str, doc_id: int):
    return es_service.get_document(index_name, doc_id)


@app.put("/update_document/")
def update_document(index_name: str, doc_id: int, document: dict):
    return es_service.update_document_by_id(index_name, doc_id, document)


@app.delete("/delete_index/")
def delete_index(index_name: str):
    return es_service.delete_index(index_name)


@app.delete("/delete_document/")
def delete_document(index_name: str, doc_id: int):
    return es_service.delete_document(index_name, doc_id)


@app.post("/search/")
def search(index_name: str, query: dict):
    return es_service.search(query, index_name)
