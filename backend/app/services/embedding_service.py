from sentence_transformers import SentenceTransformer
from ..config import Configuration
from ..logger import Logger
import os
from typing import List

logger = Logger(__name__)


class EmbeddingService:
    def __init__(self):
        self.config = Configuration().get_config('embedding')
        self.model_names = [model for model in self.config['model_names']]
        self.current_model = self.load_model(self.model_names[0])

    def set_model(self, model_name: str):
        if model_name in self.model_names:
            self.load_model(model_name)
        else:
            raise ValueError(f"Model {model_name} is not available. Choose from {list(self.model_names)}")

    def load_model(self, model_name: str):
        logger.info(f"Loading model: {model_name}")

        for model in os.listdir('./embedding_models'):
            if model == model_name:
                logger.info(f"Model already exists: {model_name}")
                return SentenceTransformer(f"./embedding_models/{model_name}")
        logger.info(f"Downloading model: {model_name}")
        self.current_model = SentenceTransformer(model_name)
        self.current_model.save(f"./embedding_models/{model_name}")
        return self.current_model

    def get_available_models(self) -> List[str]:
        return list(self.model_names)

    def encode(self, text: str):
        logger.info(f"Encoding text: {text}")
        return self.current_model.encode(text)
