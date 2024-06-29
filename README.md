# Elasticsearch Management System

## Overview
This project is an Elasticsearch management system with a FastAPI backend and a Streamlit frontend. It provides a user-friendly interface for managing Elasticsearch indices, documents, and performing various search operations.

## Features
- Create and delete Elasticsearch indices
- Insert, update, and delete documents
- Perform text and KNN (K-Nearest Neighbors) searches
- Manage index mappings
- Create and manage embeddings for semantic search
- User-friendly Streamlit interface for easy interaction

## Tech Stack
- Backend: FastAPI
- Frontend: Streamlit
- Database: Elasticsearch
- Embedding Model: [Specify the model you're using, e.g., Sentence Transformers]

## Prerequisites
- Python 3.7+
- Elasticsearch 7.x or 8.x
- pip (Python package manager)

## Installation

1. Clone the repository:
git clone ```https://github.com/MohammadMdv/Elasticseach.git```
```cd elasticsearch-management-system```
2. Set up a virtual environment (optional but recommended):
```python -m venv venv```
```source venv/bin/activate  # On Windows use venv\Scripts\activate```
3. Install the required packages:
```pip install -r requirements.txt```
4. Set up Elasticsearch:
- Ensure Elasticsearch is installed and running on your system
- Update the Elasticsearch connection settings in `app/config.py`

## Running the Application

1. Start the backend server:
```cd backend```
then
```uvicorn app.main:app --reload```


2. In a new terminal, start the Streamlit frontend:
```cd frontend```
then
```streamlit run app.py```
The Streamlit interface will open in your default web browser.

## API Documentation
Once the backend is running, you can access the API documentation at `http://localhost:8000/docs`

## Usage
1. Use the Streamlit interface to interact with the Elasticsearch management system
2. Create indices, add documents, and perform searches through the user-friendly UI
3. For advanced usage, interact directly with the FastAPI backend using the API documentation

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
