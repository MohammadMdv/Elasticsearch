from sentence_transformers import SentenceTransformer
from ..config import Configuration
from ..logger import Logger
import os

logger = Logger(__name__)


class EmbeddingService:
    def __init__(self):
        self.config = Configuration().get_config('embedding')
        self.model_name = self.config['model_name']
        self.model = self.load_model(self.model_name)

    def load_model(self, model_name: str):
        logger.info(f"Loading model: {model_name}")

        for model in os.listdir('./embedding_models'):
            if model == model_name:
                logger.info(f"Model already exists: {model_name}")
                return SentenceTransformer(f"./embedding_models/{model_name}")
        logger.info(f"Downloading model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model.save(f"./embedding_models/{model_name}")
        return self.model

    def encode(self, text: str):
        logger.info(f"Encoding text: {text}")
        return self.model.encode(text)
