from typing import Dict, Any, List

from elasticsearch import NotFoundError
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from .models.document import Document
from .models.knn_search_request import KNNRequest
from .services.elasticsearch_service import ElasticsearchService
from .services.embedding_service import EmbeddingService
from .utils.file_utils import save_uploaded_file, load_json_file

app = FastAPI()
es_service = ElasticsearchService()
embedding_service = EmbeddingService()


class IndexRequest(BaseModel):
    index_name: str
    mapping: Dict[str, Any]


class SearchRequest(BaseModel):
    index_name: str
    query: Dict[str, Any]


class EmbeddingRequest(BaseModel):
    text: str


class SetModelRequest(BaseModel):
    model_name: str


class IndexMappingRequest(BaseModel):
    index_name: str


class SemanticSearchRequest(BaseModel):
    index_name: str
    query: dict
    k: int


class IndexCreateRequest(BaseModel):
    index_name: str
    mapping: Dict[str, Any]
    semantic_fields: List[str]


class DocumentInsertRequest(BaseModel):
    index_name: str
    document: Dict[str, Any]
    semantic_fields: List[str]


@app.get("/get_vector_fields/{index_name}")
async def get_vector_fields(index_name: str):
    try:
        mappings = es_service.get_index_mapping(index_name=index_name)
        properties = mappings[index_name]['mappings']['properties']
        vector_fields = [field for field in properties.keys() if field.endswith('_vector')]
        return vector_fields
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Index not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_index_mapping/{index_name}")
async def get_index_mapping(index_name: str):
    try:
        response = es_service.get_index_mapping(index_name=index_name)
        return response
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Index not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/set_model/")
def set_model(request: SetModelRequest):
    try:
        embedding_service.set_model(request.model_name)
        return {"message": f"Model set to {request.model_name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get_available_models/")
def get_available_models():
    return {"available_models": embedding_service.get_available_models()}


@app.post("/create_index/")
async def create_index(request: IndexCreateRequest):
    try:
        # Update mapping to include vector fields for semantic fields
        for field in request.semantic_fields:
            request.mapping["properties"][f"{field}_vector"] = {
                "type": "dense_vector",
                "dims": 768
            }
        result = es_service.create_index(request.index_name, request.mapping)
        return {"message": "Index created successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/insert_document/")
async def insert_document(request: DocumentInsertRequest):
    try:
        result = es_service.insert_document(request.index_name, request.document, request.semantic_fields)
        return {"message": "Document inserted successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get_document/")
def get_document(index_name: str, doc_id):
    return es_service.get_document(index_name, doc_id)


@app.put("/update_document/")
def update_document(index_name: str, doc_id, document: Dict[str, Any]):
    return es_service.update_document_by_id(index_name, doc_id, document)


@app.delete("/delete_index/")
def delete_index(index_name: str):
    return es_service.delete_index(index_name)


@app.delete("/delete_document/")
def delete_document(index_name: str, doc_id):
    return es_service.delete_document(index_name, doc_id)


@app.post("/search/")
def search(request: SearchRequest):
    return es_service.search(request.query, request.index_name)


@app.post("/knn_search/")
def knn_search(request: KNNRequest):
    return es_service.knn_search(
        index_name=request.index_name,
        field=request.query.field,
        query_vector=embedding_service.encode(request.query.query_text),
        k=request.query.k,
        num_candidates=request.query.num_candidates
    )


@app.post("/upload_file/")
def upload_file(file: UploadFile = File(...)):
    file_path = save_uploaded_file("uploads", file)
    data = load_json_file(file_path)
    for doc in data:
        es_service.insert_one_document(doc['index_name'], doc['body'], doc.get('doc_id'))
    return {"status": "file uploaded and documents indexed"}
