from ..elasticsearch_client import ElasticsearchClient
from ..utils.decorator import handle_elasticsearch_errors
from ..logger import Logger
from elasticsearch import helpers

logger = Logger(__name__)


class ElasticsearchService:
    def __init__(self):
        self.client = ElasticsearchClient().get_client()

    @handle_elasticsearch_errors
    def create_index(self, index_name: str, mapping: dict):
        logger.info(f'Index mapping {mapping}')
        self.client.indices.create(
            index=index_name,
            body={'mappings': mapping}
        )
        logger.info(f'Created index {index_name}')
        return True

    @handle_elasticsearch_errors
    def insert_one_document(self, index_name: str, body: dict, doc_id=None):
        response = self.client.index(index=index_name, id=doc_id, body=body)
        logger.info(f"Inserted one document to {index_name} with body: {body}")
        return response

    @handle_elasticsearch_errors
    def get_document(self, index_name: str, doc_id):
        response = self.client.get(index=index_name, id=doc_id)
        logger.info(f"Getting document from index: {index_name} with id: {doc_id}")
        return response['_source']

    @handle_elasticsearch_errors
    def update_document_by_id(self, index_name: str, doc_id, body: dict):
        response = self.client.update(index=index_name, id=doc_id, body={"doc": body})
        logger.info(f"Updated document in {index_name} with id: {doc_id}")
        return response

    @handle_elasticsearch_errors
    def delete_index(self, index_name: str):
        if not self.client.indices.exists(index=index_name):
            logger.warning(f"Index {index_name} does not exist")
            return False
        try:
            self.client.indices.delete(index=index_name)
            logger.info(f'Deleted index {index_name}')
            return True
        except Exception as e:
            logger.error(f"Error deleting index {index_name}: {str(e)}")
            raise e

    @handle_elasticsearch_errors
    def delete_document(self, index_name: str, doc_id):
        response = self.client.delete(index=index_name, id=doc_id)
        logger.info(f"Deleted document {doc_id} from {index_name} index")
        return response

    @handle_elasticsearch_errors
    def delete_by_query(self, query: dict, index_name: str):
        self.client.delete_by_query(index=index_name, body={'query': query})
        logger.info(f'Deleted documents from index {index_name} that match query {query}')

    @handle_elasticsearch_errors
    def search(self, query: dict, index_name: str):
        result = self.client.search(index=index_name, body={'query': query})
        logger.info(f'Search executed on index {index_name} with query {query}')
        return result['hits']['hits']

    @handle_elasticsearch_errors
    def knn_search(self, index_name: str, field: str, query_vector: list, k: int = 2, num_candidates: int = 500):
        query = {
            "field": field,
            "query_vector": query_vector,
            "k": k,
            "num_candidates": num_candidates
        }
        response = self.client.knn_search(index=index_name, knn=query)
        logger.info(f"KNN search executed on index {index_name} with field {field}")
        return response['hits']['hits']

    @handle_elasticsearch_errors
    def count(self, index_name: str):
        self.client.indices.refresh(index=index_name)
        result = self.client.count(index=index_name)
        logger.info(f'Count executed on index {index_name}, {result["count"]} documents!')
        return result['count']

    @handle_elasticsearch_errors
    def scan_index(self, index_name: str):
        response = helpers.scan(self.client, index=index_name)
        for doc in response:
            yield doc['_source']

    @handle_elasticsearch_errors
    def bulk_index_documents(self, index_name: str, documents: list):
        actions = [{'_index': index_name, '_source': doc} for doc in documents]
        response = helpers.bulk(self.client, actions)
        logger.info(f"Bulk inserted {str(response)} documents to {index_name} index")
        return response

    @handle_elasticsearch_errors
    def get_index_mapping(self, index_name: str):
        response = self.client.indices.get_mapping(index=index_name)
        logger.info(f"Getting mapping for index {index_name}")
        return response
