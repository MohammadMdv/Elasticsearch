from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Index name and settings
index_name = "netflix_movie_vector"
index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "description": {"type": "text"},
            "description_vector": {
                "type": "dense_vector",
                "dims": 384,  # 384-dimensional vector for BERT embeddings
                "index": True,  # Enable indexing for k-NN search
                "similarity": "dot_product"  # Set similarity method
            }
        }
    }
}

# Create the index if it doesn't exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_settings)
    print(f"Index '{index_name}' created")
else:
    print(f"Index '{index_name}' already exists")

# Load the pre-trained model for embedding generation
model_name = 'sentence-transformers/paraphrase-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

# Fetch existing documents from the 'netflix_movie' index
query = {
    "query": {
        "match_all": {}
    },
    "size": 100  # Adjust the size as needed
}

response = es.search(index="netflix_movie", body=query)
descriptions = [hit['_source']['description'] for hit in response['hits']['hits']]
titles = [hit['_source']['title'] for hit in response['hits']['hits']]

# Function to normalize a vector to unit length
def normalize_vector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

# Generate and normalize embedding vectors for each description
description_vectors = [normalize_vector(model.encode(desc)).tolist() for desc in descriptions]

# Prepare documents for bulk indexing
documents = [
    {
        "_index": index_name,
        "_source": {
            "title": title,
            "description": description,
            "description_vector": description_vector
        }
    }
    for title, description, description_vector in zip(titles, descriptions, description_vectors)
]

# Index documents in bulk with detailed error handling
try:
    success, failed = helpers.bulk(es, documents, raise_on_error=False, raise_on_exception=False)
    print(f"{success} documents indexed successfully.")
    if failed:
        print(f"{len(failed)} documents failed to index.")
        for item in failed:
            action, info = item.popitem()
            print(f"Error for {action}: {info['error']['reason']}")
            if 'caused_by' in info['error']:
                print(f"Caused by: {info['error']['caused_by']['reason']}")
except Exception as e:
    print(f"Error during bulk indexing: {e}")
