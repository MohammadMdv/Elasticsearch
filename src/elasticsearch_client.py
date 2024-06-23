# built-in
import functools

# third-side
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ConnectionError, NotFoundError, RequestError

# my-own
from src.configuration import Configuration
from src.logger import Logger

logger = Logger(__name__)


def handle_elasticsearch_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFoundError as e:
            # Log a warning message for index or document not found errors
            logger.error(f"Index or document not found: {e}")
        except RequestError as e:
            # Log an error message for invalid request errors
            logger.error(f"Invalid request: {e}")
        except ConnectionError as e:
            # Connection error
            logger.error(f"Connection failed: {e}")
        except Exception as e:
            # more general error
            logger.error(f'General Error {str(e)}')

    return wrapper


class ElasticsearchClient:
    def __init__(self):
        self.config = Configuration().get_config('elasticsearch')
        self.es = self.connect_to_elastic()

    @handle_elasticsearch_errors
    def connect_to_elastic(self) -> Elasticsearch:
        es = Elasticsearch(
            f"{self.config['host']}:{self.config['port']}",
            verify_certs=False,
            basic_auth=(self.config['username'], self.config['password']))
        if es.ping():
            logger.info("Connected to Elasticsearch cluster")
            return es

    @handle_elasticsearch_errors
    def create_index(self, index_name: str, mapping: dict):
        self.es.indices.create(
            index=index_name,
            body={
                'mappings': {
                    'properties': mapping
                }
            }
        )
        logger.info(f'Created index {index_name}')
        return True

    @handle_elasticsearch_errors
    def insert_one_document(self, index_name=str, body=dict, doc_id=None):
        response = self.es.index(index=index_name, id=doc_id, body=body)
        logger.info(f"insert one document to {index_name} with body: {body}")
        return True

    @handle_elasticsearch_errors
    def get_document(self, index_name: str, doc_id: int):
        response = self.es.get(index=index_name, id=doc_id)
        logger.info(f"Getting document from index: {index_name} with id: {doc_id}")
        return response['_source']

    @handle_elasticsearch_errors
    def update_document_by_id(self, index_name: str, doc_id: int, body: dict):
        response = self.es.update(index=index_name, id=doc_id, body=body)
        logger.info(str(response))
        return True

    @handle_elasticsearch_errors
    def delete_index(self, index_name: str):
        self.es.indices.delete(index=index_name)
        logger.info(f'Deleted index {index_name}')
        return True

    @handle_elasticsearch_errors
    def delete_document(self, index_name: str, doc_id: int):
        response = self.es.delete(index=index_name, id=doc_id)
        logger.info(f"Delete document {doc_id} from {index_name} index")
        return True

    @handle_elasticsearch_errors
    def delete_by_query(self, query: dict, index_name: str):
        self.es.delete_by_query(
            index=index_name,
            body={
                'query': query
            }
        )
        logger.info(f'Deleted documents from index {index_name} that match query {query}')

    @handle_elasticsearch_errors
    def search(self, query: dict, index_name: str):
        result = self.es.search(
            index=index_name,
            body={
                'query': query
            }
        )
        logger.info(f'Search executed on index {index_name} with query {query}')
        return result['hits']['hits']

    @handle_elasticsearch_errors
    def count(self, index_name: str):
        # refresh the index
        self.es.indices.refresh(index=index_name)
        result = self.es.count(index=index_name)
        logger.info(f'Count executed on index {index_name}, {result["count"]} documents!')
        return result['count']

    @handle_elasticsearch_errors
    def scan_index(self, index_name: str):
        response = helpers.scan(self.es, index=index_name)
        for doc in response:
            yield doc['_source']

    @handle_elasticsearch_errors
    def bulk_index_documents(self, index_name: str, documents: list):
        actions = [
            {
                '_index': index_name,
                '_source': doc
            }
            for doc in documents
        ]
        response = helpers.bulk(self.es, actions)
        logger.info(f"Bulk insert {str(response)} documents to {index_name} index")
