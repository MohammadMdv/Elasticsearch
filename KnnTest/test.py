# connecting to elasticsearch and retrieving all the fields in "netflix_movie" index

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from typing import List, Dict

es = Elasticsearch("http://localhost:9200")

try:
    mappings = es.indices.get_mapping(index='netflix_movie')
    properties = mappings['netflix_movie']['mappings']['properties']
    fields = [field for field in properties.keys() if field.endswith('_vector')]
    print(fields)
except NotFoundError:
    print("Index not found")
