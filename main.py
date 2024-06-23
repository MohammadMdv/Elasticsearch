# my-own
from src.faker_class import FakerWrapper
from src.elasticsearch_client import ElasticsearchClient
from src.logger import Logger
from data.index_mapping import *

# Initialize logger
logger = Logger(__name__)

INDEX_NAME = "movie_reviews"


def main():
    es = ElasticsearchClient()

    # delete index
    es.delete_index(index_name=INDEX_NAME)
    # create index based on mapping
    es.create_index("movie_reviews", mapping=movie_review_mapping)

    fw = FakerWrapper()
    sample_data_generator = fw.generate_data(mapping=fw.mapping, num_documents=10_000)

    # insert only one document method
    es.insert_one_document(INDEX_NAME, body=next(sample_data_generator))
    es.insert_one_document(INDEX_NAME, body=next(sample_data_generator), doc_id=22)

    # insert many using bulk - insert 10 documents
    es.bulk_index_documents(index_name=INDEX_NAME, documents=[next(sample_data_generator) for _ in range(10)])

    # get document by id
    document = es.get_document(index_name=INDEX_NAME, doc_id=22)
    logger.info(f"document with id 22: {document}")

    # delete document with id == 22
    es.delete_document(index_name=INDEX_NAME, doc_id=22)

    # get count of all documents in the index (should be 1001 - we insert 1002 and delete 1)
    es.count(index_name=INDEX_NAME)

    # delete all Drama movies
    es.delete_by_query(query={"match": {"genre": "Drama"}}, index_name=INDEX_NAME)

    query = {
            "bool": {
                "must": [
                    {"match": {"genre": "Adventure"}},
                    {"range": {"imdb_rating": {"gt": 7}}}
                ]
            }
        }

    result = es.search(index_name=INDEX_NAME, query=query)
    logger.info(f"result of search: {len(result)} documents")


if __name__ == '__main__':
    main()
