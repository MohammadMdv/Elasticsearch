import faiss
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import numpy as np

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Index name containing the vectors
index_name = "netflix_movie_vector"

# Initialize SentenceTransformer model
model_name = 'sentence-transformers/paraphrase-MiniLM-L6-v2'
model = SentenceTransformer(model_name, cache_folder='cache/')

# Fetch existing documents from Elasticsearch
query = {
    "query": {
        "match_all": {}
    },
    "size": 100  # Adjust as needed
}
response = es.search(index=index_name, body=query)
descriptions = [hit['_source']['description'] for hit in response['hits']['hits']]
description_vectors = [hit['_source']['description_vector'] for hit in response['hits']['hits']]

# Convert description vectors to numpy array
description_vectors_np = np.array(description_vectors)

# Normalize vectors if necessary
# description_vectors_np = normalize(description_vectors_np, axis=1)  # Uncomment if needed

# Initialize FAISS index
index = faiss.IndexFlatL2(description_vectors_np.shape[1])  # Assuming L2 distance

# Add vectors to FAISS index
index.add(description_vectors_np.astype('float32'))

# Define the query description and convert it to a vector
query_description = "A man struggling to find his way in life..."
query_vector = model.encode(query_description).reshape(1, -1).astype('float32')

# Perform k-NN search using FAISS
k = 3  # Number of nearest neighbors to retrieve
distances, indices = index.search(query_vector, k)

# Retrieve results from Elasticsearch based on FAISS indices
search_results = []
for i in range(k):
    hit = response['hits']['hits'][indices[0][i]]
    search_results.append({
        "title": hit['_source']['title'],
        "description": hit['_source']['description'],
        "score": distances[0][i]  # Distance can be used as score
    })

# Print the search results
for result in search_results:
    print(result)
