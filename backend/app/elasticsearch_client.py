from elasticsearch import Elasticsearch
from .config import Configuration
from .logger import Logger

logger = Logger(__name__)


class ElasticsearchClient:
    def __init__(self):
        self.config = Configuration().get_config('elasticsearch')
        self.es = self.connect_to_elastic()

    def connect_to_elastic(self) -> Elasticsearch:
        es = Elasticsearch(
            f"{self.config['host']}:{self.config['port']}",
            verify_certs=False,
            basic_auth=(self.config['username'], self.config['password']))
        if es.ping():
            logger.info("Connected to Elasticsearch cluster")
        return es

    def get_client(self):
        return self.es
